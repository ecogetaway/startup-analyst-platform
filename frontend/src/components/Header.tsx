import React from 'react';
import { RocketLaunchIcon, ChartBarIcon, ShieldCheckIcon } from '@heroicons/react/24/outline';

const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg">
              <RocketLaunchIcon className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Startup Analyst</h1>
              <p className="text-sm text-gray-500">AI-Powered Investment Analysis</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <ChartBarIcon className="w-4 h-4" />
              <span>Multi-Agent Analysis</span>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <ShieldCheckIcon className="w-4 h-4" />
              <span>Google AI Powered</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
