import React from 'react';
import { PlayIcon, SparklesIcon } from '@heroicons/react/24/outline';

interface DemoScenario {
  id: string;
  name: string;
  description: string;
  data: any;
}

interface DemoScenariosProps {
  scenarios: DemoScenario[];
  onSelectScenario: (scenario: DemoScenario) => void;
}

const DemoScenarios: React.FC<DemoScenariosProps> = ({ scenarios, onSelectScenario }) => {
  if (scenarios.length === 0) return null;

  return (
    <div className="mb-8">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          🎯 Try Demo Scenarios
        </h2>
        <p className="text-gray-600">
          Click on any scenario below to see the AI analysis in action
        </p>
      </div>
      
      <div className="grid md:grid-cols-3 gap-6">
        {scenarios.map((scenario) => (
          <div
            key={scenario.id}
            className="card hover:shadow-lg transition-shadow duration-200 cursor-pointer group"
            onClick={() => onSelectScenario(scenario)}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-2">
                <SparklesIcon className="w-5 h-5 text-primary-600" />
                <h3 className="font-semibold text-gray-900">{scenario.name}</h3>
              </div>
              <PlayIcon className="w-5 h-5 text-gray-400 group-hover:text-primary-600 transition-colors" />
            </div>
            
            <p className="text-gray-600 text-sm mb-4">{scenario.description}</p>
            
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-500">
                Company: {scenario.data.company_name}
              </span>
              <button className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                Analyze →
              </button>
            </div>
          </div>
        ))}
      </div>
      
      <div className="text-center mt-6">
        <div className="inline-flex items-center px-4 py-2 bg-gray-100 rounded-full">
          <span className="text-sm text-gray-600">Or enter your own startup details below</span>
        </div>
      </div>
    </div>
  );
};

export default DemoScenarios;
