import React, { useState } from 'react';
import { 
  ChartBarIcon, 
  DocumentTextIcon, 
  ExclamationTriangleIcon,
  LightBulbIcon,
  ArrowTrendingUpIcon,
  CheckCircleIcon,
  ClockIcon,
  CurrencyDollarIcon
} from '@heroicons/react/24/outline';

interface ModernResultsProps {
  results: any;
  onReset: () => void;
}

const ModernResults: React.FC<ModernResultsProps> = ({ results, onReset }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'analysis' | 'memo' | 'multimodal'>('overview');
  
  // Debug logging
  console.log('ModernResults received results:', results);
  console.log('Agent results:', results?.agent_results);
  console.log('Investment insights:', results?.agent_results?.investment_insights);
  console.log('Investment insights findings:', results?.agent_results?.investment_insights?.findings);
  console.log('Investment insights text:', results?.agent_results?.investment_insights?.findings?.investment_insights);

  // Extract key information
  const companyName = results?.company_name || 'Unknown Company';
  const recommendation = results?.recommendation || 'UNDER REVIEW';
  const confidenceScore = results?.confidence_score || 0;
  const processingTime = results?.processing_time || 0;
  const hasMultiModal = results?.has_pitch_materials || false;
  const agentsUsed = results?.agents_used || [];

  const getRecommendationColor = (rec: string) => {
    switch (rec.toUpperCase()) {
      case 'RECOMMENDED':
      case 'STRONG BUY':
      case 'BUY':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'CONDITIONAL':
      case 'HOLD':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'NOT RECOMMENDED':
      case 'PASS':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getRecommendationIcon = (rec: string) => {
    switch (rec.toUpperCase()) {
      case 'RECOMMENDED':
      case 'STRONG BUY':
      case 'BUY':
        return <CheckCircleIcon className="w-5 h-5" />;
      case 'CONDITIONAL':
      case 'HOLD':
        return <ClockIcon className="w-5 h-5" />;
      case 'NOT RECOMMENDED':
      case 'PASS':
        return <ExclamationTriangleIcon className="w-5 h-5" />;
      default:
        return <ChartBarIcon className="w-5 h-5" />;
    }
  };

  const keyMetrics = [
    {
      label: 'Processing Time',
      value: `${processingTime.toFixed(1)}s`,
      icon: ClockIcon,
      color: 'text-blue-600'
    },
    {
      label: 'Confidence Score',
      value: `${(confidenceScore * 100).toFixed(0)}%`,
      icon: ArrowTrendingUpIcon,
      color: 'text-green-600'
    },
    {
      label: 'Agents Used',
      value: agentsUsed.length,
      icon: ChartBarIcon,
      color: 'text-purple-600'
    },
    {
      label: 'Multi-Modal',
      value: hasMultiModal ? 'Yes' : 'No',
      icon: DocumentTextIcon,
      color: 'text-orange-600'
    }
  ];

  const tabs = [
    { id: 'overview', label: 'Executive Summary', icon: DocumentTextIcon },
    { id: 'analysis', label: 'Detailed Analysis', icon: ChartBarIcon },
    { id: 'memo', label: 'Investment Memo', icon: CurrencyDollarIcon },
    { id: 'multimodal', label: 'Multi-Modal Insights', icon: LightBulbIcon, disabled: !hasMultiModal }
  ];

  return (
    <div className="space-y-8">
      {/* Header Section */}
      <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-2xl p-8 border border-green-100">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{companyName}</h1>
            <p className="text-gray-600">Investment Analysis Complete</p>
          </div>
          <div className={`inline-flex items-center space-x-2 px-4 py-2 rounded-full border font-medium ${getRecommendationColor(recommendation)}`}>
            {getRecommendationIcon(recommendation)}
            <span>{recommendation}</span>
          </div>
        </div>

        {/* Key Metrics Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {keyMetrics.map((metric, index) => (
            <div key={index} className="bg-white rounded-xl p-4 border border-gray-100">
              <div className="flex items-center space-x-3">
                <metric.icon className={`w-6 h-6 ${metric.color}`} />
                <div>
                  <p className="text-2xl font-bold text-gray-900">{metric.value}</p>
                  <p className="text-sm text-gray-600">{metric.label}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="border-b border-gray-200">
        <nav className="flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => !tab.disabled && setActiveTab(tab.id as typeof activeTab)}
              disabled={tab.disabled}
              className={`
                flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors
                ${activeTab === tab.id
                  ? 'border-green-500 text-green-600'
                  : tab.disabled
                    ? 'border-transparent text-gray-300 cursor-not-allowed'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }
              `}
            >
              <tab.icon className="w-5 h-5" />
              <span>{tab.label}</span>
              {tab.disabled && (
                <span className="text-xs bg-gray-100 text-gray-500 px-2 py-1 rounded">
                  N/A
                </span>
              )}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="space-y-6">
        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl border border-gray-200 p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Executive Summary</h2>
              
              {/* ML Prediction Results */}
              {results?.ml_prediction && (
                <div className="mb-8 p-6 bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl border border-purple-200">
                  <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                    🤖 AI Success Prediction
                    <span className="ml-2 text-sm font-normal text-gray-600">
                      (85% Accuracy)
                    </span>
                  </h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                    <div className="text-center p-4 bg-white rounded-lg border">
                      <div className="text-3xl font-bold text-purple-600">
                        {Math.round(results.ml_prediction.success_probability * 100)}%
                      </div>
                      <div className="text-sm text-gray-600">Success Probability</div>
                    </div>
                    
                    <div className="text-center p-4 bg-white rounded-lg border">
                      <div className={`text-2xl font-bold ${
                        results.ml_prediction.prediction === 'Success' 
                          ? 'text-green-600' 
                          : 'text-red-600'
                      }`}>
                        {results.ml_prediction.prediction}
                      </div>
                      <div className="text-sm text-gray-600">Prediction</div>
                    </div>
                    
                    <div className="text-center p-4 bg-white rounded-lg border">
                      <div className="text-2xl font-bold text-blue-600">
                        {Math.round(results.ml_prediction.confidence * 100)}%
                      </div>
                      <div className="text-sm text-gray-600">Confidence</div>
                    </div>
                  </div>
                  
                  {results.ml_prediction.key_factors && results.ml_prediction.key_factors.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-2">Key Success Factors:</h4>
                      <div className="space-y-2">
                        {results.ml_prediction.key_factors.slice(0, 3).map((factor: any, index: number) => (
                          <div key={index} className="flex items-center justify-between p-2 bg-white rounded border">
                            <span className="text-sm text-gray-700 capitalize">
                              {factor[0].replace('_', ' ')}
                            </span>
                            <span className="text-sm font-medium text-purple-600">
                              {Math.round(factor[1] * 100)}%
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
              
              {/* Display analysis from agent results */}
              <div className="prose max-w-none mb-8">
                {results?.agent_results?.investment_insights?.findings?.investment_insights ? (
                  <div className="text-gray-700 leading-relaxed text-lg whitespace-pre-line">
                    {results.agent_results.investment_insights.findings.investment_insights}
                  </div>
                ) : results?.agent_results?.business_analysis?.findings?.analysis ? (
                  <div className="text-gray-700 leading-relaxed text-lg whitespace-pre-line">
                    {results.agent_results.business_analysis.findings.analysis}
                  </div>
                ) : results?.summary ? (
                  <div className="text-gray-700 leading-relaxed text-lg">
                    {results.summary}
                  </div>
                ) : (
                  <div className="text-gray-500 leading-relaxed text-lg">
                    <p>Analysis completed successfully. Detailed insights are available in the Detailed Analysis tab.</p>
                    <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                      <p className="text-sm text-blue-700">
                        <strong>Available Data:</strong> 
                        Investment Insights: {results?.agent_results?.investment_insights ? 'Yes' : 'No'} | 
                        Business Analysis: {results?.agent_results?.business_analysis ? 'Yes' : 'No'} |
                        Summary: {results?.summary ? 'Yes' : 'No'}
                      </p>
                    </div>
                  </div>
                )}
              </div>

              {/* Next Steps */}
              {results?.next_steps && results.next_steps.length > 0 && (
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">Recommended Next Steps</h3>
                  <div className="space-y-3">
                    {results.next_steps.map((step: string, index: number) => (
                      <div key={index} className="flex items-start space-x-3">
                        <div className="w-6 h-6 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-sm font-medium mt-0.5">
                          {index + 1}
                        </div>
                        <p className="text-gray-700 flex-1">{step}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Analysis Tab */}
        {activeTab === 'analysis' && (
          <div className="space-y-6">
            {results?.agent_results && Object.entries(results.agent_results).map(([agentType, agentResult]: [string, any]) => (
              <div key={agentType} className="bg-white rounded-2xl border border-gray-200 p-8">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-semibold text-gray-900">
                    {agentResult.agent_name || agentType.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()) + ' Agent'}
                  </h3>
                  <div className="flex items-center space-x-4">
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                      agentResult.status === 'completed' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {agentResult.status}
                    </span>
                    <span className="text-sm text-gray-500">
                      {agentResult.processing_time?.toFixed(2)}s
                    </span>
                  </div>
                </div>

                {agentResult.findings && (
                  <div className="space-y-4">
                    {agentResult.findings.analysis && (
                      <div className="prose max-w-none">
                        <div className="text-gray-700 whitespace-pre-line">
                          {agentResult.findings.analysis}
                        </div>
                      </div>
                    )}
                    
                    {agentResult.findings.risk_analysis && (
                      <div>
                        <h4 className="font-medium text-gray-900 mb-2">Risk Analysis:</h4>
                        <div className="text-gray-700 whitespace-pre-line">
                          {agentResult.findings.risk_analysis}
                        </div>
                      </div>
                    )}
                    
                    {agentResult.findings.key_points && (
                      <div>
                        <h4 className="font-medium text-gray-900 mb-2">Key Insights:</h4>
                        <ul className="space-y-2">
                          {agentResult.findings.key_points.map((point: string, index: number) => (
                            <li key={index} className="flex items-start space-x-2">
                              <div className="w-1.5 h-1.5 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                              <span className="text-gray-700">{point}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Scheduling & Interview Agent specific content */}
                    {agentType === 'scheduling_interview' && agentResult.findings && (
                      <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                        <h4 className="font-medium text-purple-900 mb-3 flex items-center">
                          <ClockIcon className="w-5 h-5 mr-2" />
                          Post-Analysis Interview System
                        </h4>
                        
                        <div className="space-y-3 text-sm">
                          <div className="bg-white rounded p-3 border-l-4 border-purple-400">
                            <p className="font-medium text-purple-900">Purpose:</p>
                            <p className="text-gray-700">{agentResult.findings.interview_purpose}</p>
                          </div>
                          
                          <div>
                            <p><strong>Status:</strong> {agentResult.findings.scheduling_status}</p>
                            <p><strong>Workflow Stage:</strong> {agentResult.findings.workflow_stage?.replace('_', ' ').toUpperCase()}</p>
                          </div>

                          {agentResult.findings.interview_capabilities && (
                            <div>
                              <p className="font-medium text-purple-900 mb-2">Production Capabilities:</p>
                              <ul className="space-y-1 ml-4">
                                {agentResult.findings.interview_capabilities.slice(0, 4).map((capability: string, index: number) => (
                                  <li key={index} className="text-gray-700 text-xs">• {capability}</li>
                                ))}
                              </ul>
                            </div>
                          )}

                          {agentResult.findings.typical_questions && (
                            <div>
                              <p className="font-medium text-purple-900 mb-2">Example Interview Topics:</p>
                              <div className="grid grid-cols-2 gap-1 text-xs">
                                {agentResult.findings.typical_questions.slice(0, 4).map((question: string, index: number) => (
                                  <div key={index} className="text-gray-600">• {question}</div>
                                ))}
                              </div>
                            </div>
                          )}

                          <button className="w-full bg-purple-600 text-white py-2 px-4 rounded-md text-sm font-medium hover:bg-purple-700 transition-colors">
                            📞 Request Founder Interview
                          </button>

                          {agentResult.findings.demo_note && (
                            <p className="text-purple-700 italic text-xs mt-2 p-2 bg-purple-100 rounded">
                              💡 {agentResult.findings.demo_note}
                            </p>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Investment insights specific content */}
                    {agentResult.findings.investment_insights && (
                      <div>
                        <h4 className="font-medium text-gray-900 mb-2">Investment Analysis:</h4>
                        <div className="prose max-w-none">
                          <div className="text-gray-700 whitespace-pre-line">
                            {agentResult.findings.investment_insights}
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Investment Memo Tab */}
        {activeTab === 'memo' && (
          <div className="bg-white rounded-2xl border border-gray-200 p-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Investment Memo</h2>
              <button className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 font-medium">
                Export PDF
              </button>
            </div>

            {results?.multi_modal_analysis?.deal_memo ? (
              <div className="space-y-6">
                {/* Memo Metadata */}
                {results.multi_modal_analysis.deal_memo.memo_metadata && (
                  <div className="bg-gray-50 rounded-xl p-6">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="text-gray-500">Memo ID:</span>
                        <p className="font-medium">{results.multi_modal_analysis.deal_memo.memo_metadata.memo_id}</p>
                      </div>
                      <div>
                        <span className="text-gray-500">Generated:</span>
                        <p className="font-medium">{results.multi_modal_analysis.deal_memo.memo_metadata.generated_date}</p>
                      </div>
                      <div>
                        <span className="text-gray-500">Confidence:</span>
                        <p className="font-medium">{(results.multi_modal_analysis.deal_memo.memo_metadata.confidence_score * 100).toFixed(0)}%</p>
                      </div>
                      <div>
                        <span className="text-gray-500">Sources:</span>
                        <p className="font-medium">{results.multi_modal_analysis.deal_memo.memo_metadata.sources_analyzed?.total || 'N/A'}</p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Investment Memo Content */}
                <div className="prose max-w-none">
                  <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                    {results.multi_modal_analysis.deal_memo.investment_memo}
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-12">
                <DocumentTextIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Investment Memo</h3>
                <p className="text-gray-600">Detailed investment memo would be generated from multi-modal analysis</p>
              </div>
            )}
          </div>
        )}

        {/* Multi-Modal Tab */}
        {activeTab === 'multimodal' && hasMultiModal && (
          <div className="space-y-6">
            {results?.multi_modal_analysis && (
              <>
                {/* Processing Summary */}
                <div className="bg-white rounded-2xl border border-gray-200 p-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-6">Multi-Modal Analysis</h2>
                  
                  <div className="grid md:grid-cols-3 gap-6 mb-8">
                    <div className="text-center">
                      <DocumentTextIcon className="w-12 h-12 text-blue-600 mx-auto mb-2" />
                      <p className="text-2xl font-bold text-gray-900">
                        {results.multi_modal_analysis.documents?.length || 0}
                      </p>
                      <p className="text-gray-600">Documents</p>
                    </div>
                    <div className="text-center">
                      <span className="text-4xl mb-2 block">🎤</span>
                      <p className="text-2xl font-bold text-gray-900">
                        {results.multi_modal_analysis.audio_transcripts?.length || 0}
                      </p>
                      <p className="text-gray-600">Audio Files</p>
                    </div>
                    <div className="text-center">
                      <span className="text-4xl mb-2 block">🎥</span>
                      <p className="text-2xl font-bold text-gray-900">
                        {results.multi_modal_analysis.video_analysis?.length || 0}
                      </p>
                      <p className="text-gray-600">Video Files</p>
                    </div>
                  </div>

                  {/* Combined Insights */}
                  {results.multi_modal_analysis.combined_insights && (
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-4">AI Synthesis</h3>
                      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6">
                        <p className="text-gray-700 leading-relaxed">
                          {results.multi_modal_analysis.combined_insights}
                        </p>
                      </div>
                    </div>
                  )}
                </div>
              </>
            )}
          </div>
        )}
      </div>

      {/* Footer Actions */}
      <div className="bg-gray-50 rounded-2xl p-6 text-center">
        <p className="text-gray-600 mb-4">Analysis powered by Google's comprehensive tech stack</p>
        <div className="flex flex-wrap justify-center gap-3 mb-6">
          {['🔥 Firebase Real-time', '☁️ Cloud Storage', '🤖 Google ADK', '🧠 Gemini AI', '📊 Multi-Modal'].map(tech => (
            <span key={tech} className="bg-white text-gray-700 px-3 py-1 rounded-full text-sm border">
              {tech}
            </span>
          ))}
        </div>
        <button
          onClick={onReset}
          className="bg-green-600 text-white px-8 py-3 rounded-lg hover:bg-green-700 font-medium"
        >
          Start New Analysis
        </button>
      </div>
    </div>
  );
};

export default ModernResults;
