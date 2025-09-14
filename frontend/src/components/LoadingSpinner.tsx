import React from 'react';
import { ChartBarIcon, UserGroupIcon, ShieldCheckIcon, LightBulbIcon, DocumentTextIcon } from '@heroicons/react/24/outline';

const LoadingSpinner: React.FC = () => {
  const agents = [
    { name: 'Data Collection', icon: ChartBarIcon, color: 'text-blue-600' },
    { name: 'Business Analysis', icon: UserGroupIcon, color: 'text-green-600' },
    { name: 'Risk Assessment', icon: ShieldCheckIcon, color: 'text-yellow-600' },
    { name: 'Investment Insights', icon: LightBulbIcon, color: 'text-purple-600' },
    { name: 'Report Generation', icon: DocumentTextIcon, color: 'text-red-600' },
  ];

  return (
    <div className="card text-center">
      <div className="mb-6">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full mb-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
        </div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          🤖 AI Analysis in Progress
        </h2>
        <p className="text-gray-600">
          Our AI agents are analyzing your startup data. This may take a few minutes...
        </p>
      </div>

      <div className="space-y-4">
        <div className="text-sm text-gray-500 mb-4">
          Running 5 specialized AI agents in parallel:
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {agents.map((agent, index) => {
            const IconComponent = agent.icon;
            return (
              <div key={agent.name} className="flex flex-col items-center p-4 bg-gray-50 rounded-lg">
                <IconComponent className={`w-8 h-8 ${agent.color} mb-2 animate-pulse`} />
                <span className="text-sm font-medium text-gray-700">{agent.name}</span>
                <div className="mt-2 w-full bg-gray-200 rounded-full h-1">
                  <div className="bg-blue-600 h-1 rounded-full animate-pulse" style={{ width: '60%' }}></div>
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <div className="flex items-center justify-center space-x-2 text-blue-700">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
            <span className="text-sm font-medium">Processing with Google's Gemini AI...</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;
