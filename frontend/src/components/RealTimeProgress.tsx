import React, { useState, useEffect } from 'react';
import { CheckCircleIcon, ClockIcon, ExclamationCircleIcon } from '@heroicons/react/24/outline';

interface ProgressData {
  progress: number;
  current_agent: string | null;
  status: string;
  agents_completed: string[];
  results?: Record<string, any>;
  updated_at: number;
}

interface RealTimeProgressProps {
  startupId: string;
  onComplete?: (results: any) => void;
}

const agentDisplayNames: Record<string, string> = {
  'data_collection': 'Data Collection',
  'business_analysis': 'Business Analysis',
  'risk_assessment': 'Risk Assessment',
  'investment_insights': 'Investment Insights',
  'report_generation': 'Report Generation'
};

const agentDescriptions: Record<string, string> = {
  'data_collection': 'Gathering market data and company information',
  'business_analysis': 'Analyzing business model and competitive positioning',
  'risk_assessment': 'Evaluating potential risks and mitigation strategies',
  'investment_insights': 'Generating investment recommendations and valuation',
  'report_generation': 'Creating comprehensive executive summary'
};

const RealTimeProgress: React.FC<RealTimeProgressProps> = ({ startupId, onComplete }) => {
  const [progressData, setProgressData] = useState<ProgressData>({
    progress: 0,
    current_agent: null,
    status: 'initiated',
    agents_completed: [],
    updated_at: Date.now()
  });
  
  const [startTime] = useState(Date.now());
  const [elapsedTime, setElapsedTime] = useState(0);

  // Simulate real-time updates (in production, this would use Firebase listeners)
  useEffect(() => {
    const pollProgress = async () => {
      try {
        const response = await fetch(`/api/analysis-progress/${startupId}`);
        if (response.ok) {
          const data = await response.json();
          setProgressData(data);
          
          if (data.status === 'completed' && data.progress >= 100) {
            if (onComplete && data.results) {
              onComplete(data.results);
            }
          }
        }
      } catch (error) {
        console.error('Failed to fetch progress:', error);
      }
    };

    // Initial fetch
    pollProgress();

    // Poll every 2 seconds
    const interval = setInterval(pollProgress, 2000);

    return () => clearInterval(interval);
  }, [startupId, onComplete]);

  // Update elapsed time
  useEffect(() => {
    const timer = setInterval(() => {
      setElapsedTime(Date.now() - startTime);
    }, 1000);

    return () => clearInterval(timer);
  }, [startTime]);

  const formatTime = (milliseconds: number): string => {
    const seconds = Math.floor(milliseconds / 1000);
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    
    if (minutes > 0) {
      return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
    return `${remainingSeconds}s`;
  };

  const getAgentStatus = (agentKey: string) => {
    if (progressData.agents_completed && progressData.agents_completed.includes(agentKey)) {
      return 'completed';
    } else if (progressData.current_agent === agentKey) {
      return 'in_progress';
    } else {
      return 'pending';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'in_progress':
        return <ClockIcon className="h-5 w-5 text-blue-500 animate-spin" />;
      case 'failed':
        return <ExclamationCircleIcon className="h-5 w-5 text-red-500" />;
      default:
        return <div className="h-5 w-5 rounded-full border-2 border-gray-300" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-green-700 bg-green-50 border-green-200';
      case 'in_progress':
        return 'text-blue-700 bg-blue-50 border-blue-200';
      case 'failed':
        return 'text-red-700 bg-red-50 border-red-200';
      default:
        return 'text-gray-700 bg-gray-50 border-gray-200';
    }
  };

  const agents = Object.keys(agentDisplayNames);

  return (
    <div className="bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-white">AI Analysis in Progress</h3>
            <p className="text-blue-100 text-sm">Google ADK Multi-Agent System</p>
          </div>
          <div className="text-right text-white">
            <div className="text-2xl font-bold">{progressData.progress}%</div>
            <div className="text-xs text-blue-100">Elapsed: {formatTime(elapsedTime)}</div>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="w-full bg-gray-200 rounded-full h-3 mb-2">
          <div 
            className="bg-gradient-to-r from-blue-600 to-purple-600 h-3 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${progressData.progress}%` }}
          ></div>
        </div>
        <div className="flex justify-between text-xs text-gray-600">
          <span>Starting Analysis</span>
          <span>Complete</span>
        </div>
      </div>

      {/* Agent Progress */}
      <div className="px-6 py-4">
        <h4 className="text-sm font-medium text-gray-900 mb-4">🤖 Agent Progress</h4>
        <div className="space-y-3">
          {agents.map((agentKey, index) => {
            const status = getAgentStatus(agentKey);
            const displayName = agentDisplayNames[agentKey];
            const description = agentDescriptions[agentKey];
            
            return (
              <div
                key={agentKey}
                className={`
                  flex items-start space-x-3 p-3 rounded-lg border transition-all duration-300
                  ${getStatusColor(status)}
                `}
              >
                <div className="flex-shrink-0 mt-0.5">
                  {getStatusIcon(status)}
                </div>
                <div className="flex-grow min-w-0">
                  <div className="flex items-center justify-between">
                    <h5 className="text-sm font-medium truncate">
                      {index + 1}. {displayName}
                    </h5>
                    {status === 'completed' && (
                      <span className="text-xs font-medium text-green-600">✓ Done</span>
                    )}
                    {status === 'in_progress' && (
                      <span className="text-xs font-medium text-blue-600">⚡ Working</span>
                    )}
                  </div>
                  <p className="text-xs mt-1 text-current opacity-75">
                    {description}
                  </p>
                  
                  {/* Show results if available */}
                  {status === 'completed' && progressData.results?.[agentKey] && (
                    <div className="mt-2 text-xs">
                      <span className="font-medium">Key Insights:</span>
                      <ul className="list-disc list-inside mt-1 space-y-0.5 opacity-75">
                        <li>Analysis completed successfully</li>
                        <li>Data processed and validated</li>
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Current Status */}
      <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="h-2 w-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-700">
              {progressData.current_agent 
                ? `Processing: ${agentDisplayNames[progressData.current_agent] || progressData.current_agent}`
                : progressData.status === 'completed' 
                  ? 'Analysis Complete!' 
                  : 'Initializing analysis...'
              }
            </span>
          </div>
          <div className="text-xs text-gray-500">
            Last updated: {new Date(progressData.updated_at).toLocaleTimeString()}
          </div>
        </div>
      </div>

      {/* Tech Stack Info */}
      <div className="px-6 py-3 bg-blue-50 border-t border-blue-200">
        <div className="flex items-center justify-center space-x-4 text-xs text-blue-700">
          <span>🔥 Firebase Real-time</span>
          <span>•</span>
          <span>🤖 Google ADK</span>
          <span>•</span>
          <span>🧠 Gemini AI</span>
          <span>•</span>
          <span>☁️ Cloud Storage</span>
        </div>
      </div>
    </div>
  );
};

export default RealTimeProgress;
