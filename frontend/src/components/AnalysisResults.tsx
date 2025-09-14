import React, { useState } from 'react';
import { AnalysisResults as AnalysisResultsType } from '../types';
import { 
  ChartBarIcon, 
  UserGroupIcon, 
  ShieldCheckIcon, 
  LightBulbIcon, 
  DocumentTextIcon,
  ArrowPathIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';

interface AnalysisResultsProps {
  results: AnalysisResultsType;
  onReset: () => void;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ results, onReset }) => {
  const [activeTab, setActiveTab] = useState('overview');

  const getRecommendationColor = (recommendation: string) => {
    switch (recommendation) {
      case 'INVEST': return 'text-green-600 bg-green-100';
      case 'PASS': return 'text-red-600 bg-red-100';
      case 'WATCH': return 'text-yellow-600 bg-yellow-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'LOW': return 'text-green-600 bg-green-100';
      case 'MEDIUM': return 'text-yellow-600 bg-yellow-100';
      case 'HIGH': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const tabs = [
    { id: 'overview', name: 'Overview', icon: ChartBarIcon },
    { id: 'market', name: 'Market Analysis', icon: UserGroupIcon },
    { id: 'business', name: 'Business Model', icon: LightBulbIcon },
    { id: 'risks', name: 'Risk Assessment', icon: ShieldCheckIcon },
    { id: 'investment', name: 'Investment Insights', icon: DocumentTextIcon },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              📊 Analysis Results
            </h1>
            <p className="text-gray-600">
              Comprehensive AI analysis for <strong>{results.startup_input.company_name}</strong>
            </p>
          </div>
          <button
            onClick={onReset}
            className="btn-secondary flex items-center space-x-2"
          >
            <ArrowPathIcon className="w-4 h-4" />
            <span>New Analysis</span>
          </button>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="text-sm text-gray-500 mb-1">Recommendation</div>
            <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getRecommendationColor(results.investment_insights.recommendation)}`}>
              {results.investment_insights.recommendation}
            </div>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="text-sm text-gray-500 mb-1">Confidence Score</div>
            <div className="text-2xl font-bold text-gray-900">
              {results.investment_insights.confidence_score}/10
            </div>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="text-sm text-gray-500 mb-1">Processing Time</div>
            <div className="text-2xl font-bold text-gray-900">
              {results.processing_time.toFixed(1)}s
            </div>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="text-sm text-gray-500 mb-1">Analysis Date</div>
            <div className="text-sm font-medium text-gray-900">
              {new Date(results.analysis_timestamp).toLocaleDateString()}
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="card">
        <div className="border-b border-gray-200 mb-6">
          <nav className="-mb-px flex space-x-8">
            {tabs.map((tab) => {
              const IconComponent = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <IconComponent className="w-4 h-4" />
                  <span>{tab.name}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="min-h-[400px]">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Investment Recommendation</h3>
                <div className={`inline-flex items-center px-4 py-2 rounded-lg text-lg font-medium ${getRecommendationColor(results.investment_insights.recommendation)}`}>
                  {results.investment_insights.recommendation}
                </div>
                <p className="mt-2 text-gray-600">
                  Confidence Score: {results.investment_insights.confidence_score}/10
                </p>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Key Investment Thesis</h3>
                <ul className="space-y-2">
                  {results.investment_insights.key_thesis.map((thesis, index) => (
                    <li key={index} className="flex items-start space-x-2">
                      <CheckCircleIcon className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-700">{thesis}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Due Diligence Priorities</h3>
                <ul className="space-y-2">
                  {results.investment_insights.due_diligence_priorities.map((priority, index) => (
                    <li key={index} className="flex items-start space-x-2">
                      <ExclamationTriangleIcon className="w-5 h-5 text-yellow-500 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-700">{priority}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {activeTab === 'market' && (
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Market Analysis</h3>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-500">Market Size</label>
                    <p className="text-gray-900">{results.market_analysis.market_size || 'Not specified'}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Growth Rate</label>
                    <p className="text-gray-900">{results.market_analysis.growth_rate || 'Not specified'}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Competition Level</label>
                    <p className="text-gray-900">{results.market_analysis.competition_level || 'Not specified'}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Target Customers</label>
                    <p className="text-gray-900">{results.market_analysis.target_customers || 'Not specified'}</p>
                  </div>
                </div>
                {results.market_analysis.market_trends && (
                  <div className="mt-4">
                    <label className="text-sm font-medium text-gray-500">Market Trends</label>
                    <p className="text-gray-900">{results.market_analysis.market_trends}</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'business' && (
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Business Model Analysis</h3>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-500">Revenue Model</label>
                    <p className="text-gray-900">{results.business_model_analysis.revenue_model || 'Not specified'}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Scalability</label>
                    <p className="text-gray-900">{results.business_model_analysis.scalability || 'Not specified'}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Competitive Advantage</label>
                    <p className="text-gray-900">{results.business_model_analysis.competitive_advantage || 'Not specified'}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Monetization Strategy</label>
                    <p className="text-gray-900">{results.business_model_analysis.monetization_strategy || 'Not specified'}</p>
                  </div>
                </div>
                {results.business_model_analysis.unit_economics && (
                  <div className="mt-4">
                    <label className="text-sm font-medium text-gray-500">Unit Economics</label>
                    <p className="text-gray-900">{results.business_model_analysis.unit_economics}</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'risks' && (
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Risk Assessment</h3>
                <div className="grid md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="text-sm font-medium text-gray-500">Market Risk</label>
                    <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(results.risk_assessment.market_risk)}`}>
                      {results.risk_assessment.market_risk}
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Technology Risk</label>
                    <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(results.risk_assessment.technology_risk)}`}>
                      {results.risk_assessment.technology_risk}
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Financial Risk</label>
                    <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(results.risk_assessment.financial_risk)}`}>
                      {results.risk_assessment.financial_risk}
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Team Risk</label>
                    <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(results.risk_assessment.team_risk)}`}>
                      {results.risk_assessment.team_risk}
                    </div>
                  </div>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Risk Summary</label>
                  <p className="text-gray-900">{results.risk_assessment.risk_summary}</p>
                </div>
                {results.risk_assessment.mitigation_strategies.length > 0 && (
                  <div className="mt-4">
                    <label className="text-sm font-medium text-gray-500">Mitigation Strategies</label>
                    <ul className="mt-2 space-y-1">
                      {results.risk_assessment.mitigation_strategies.map((strategy, index) => (
                        <li key={index} className="flex items-start space-x-2">
                          <ShieldCheckIcon className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
                          <span className="text-gray-700">{strategy}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'investment' && (
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Investment Insights</h3>
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-gray-500">Valuation Considerations</label>
                    <p className="text-gray-900">{results.investment_insights.valuation_considerations || 'Not specified'}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Exit Potential</label>
                    <p className="text-gray-900">{results.investment_insights.exit_potential || 'Not specified'}</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AnalysisResults;
