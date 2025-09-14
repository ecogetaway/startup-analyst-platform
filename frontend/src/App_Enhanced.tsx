import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import StartupForm from './components/StartupForm';
import AnalysisResults from './components/AnalysisResults';
import DemoScenarios from './components/DemoScenarios';
import LoadingSpinner from './components/LoadingSpinner';
import FileUpload from './components/FileUpload';
import RealTimeProgress from './components/RealTimeProgress';
import { analyzeStartup } from './services/api';
import { StartupInput, AnalysisResults as AnalysisResultsType } from './types';

interface UploadedFile {
  name: string;
  size: number;
  type: string;
  public_url: string;
  storage_path: string;
  timestamp: number;
}

const AppEnhanced: React.FC = () => {
  const [results, setResults] = useState<AnalysisResultsType | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentStartupId, setCurrentStartupId] = useState<string | null>(null);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [showRealTimeProgress, setShowRealTimeProgress] = useState(false);

  // Demo scenarios data
  const [demoScenarios, setDemoScenarios] = useState([
    {
      id: "high-potential",
      name: "High-Potential AI Startup",
      description: "AI-powered healthcare platform with strong team and market opportunity",
      data: {
        company_name: "MedAI Solutions",
        business_description: "AI-powered diagnostic platform that helps doctors identify diseases from medical images with 95% accuracy. Our platform reduces diagnosis time by 70% and improves patient outcomes.",
        industry: "Healthcare AI",
        stage: "Series A",
        founder_name: "Dr. Sarah Chen",
        founder_background: "Former Google AI researcher with 10 years in medical imaging. PhD in Computer Science from Stanford. Published 50+ papers in top-tier journals.",
        website: "https://medai-solutions.com",
        additional_info: "Raised $5M seed round. 50+ hospital partnerships. FDA approval in progress."
      }
    },
    {
      id: "clean-tech",
      name: "Clean Technology Startup",
      description: "Electric vehicle charging network powered by renewable energy",
      data: {
        company_name: "EcoTransport Solutions",
        business_description: "Electric vehicle charging network powered by renewable energy sources. Our smart charging stations optimize energy usage and provide real-time availability tracking.",
        industry: "Clean Technology",
        stage: "Series A",
        founder_name: "Alex Rodriguez",
        founder_background: "Former Tesla engineer with 12 years in EV technology. MBA from Stanford. Previous startup experience in renewable energy.",
        website: "https://ecotransport.com",
        additional_info: "75 charging stations deployed. Partnerships with 5 cities. $150K monthly revenue."
      }
    },
    {
      id: "fintech",
      name: "FinTech B2B Platform",
      description: "Automated financial planning for small businesses",
      data: {
        company_name: "FinanceFlow",
        business_description: "Automated financial planning and cash flow management platform for small businesses. Uses AI to predict cash flow needs and optimize financial decisions.",
        industry: "Financial Technology",
        stage: "Series B",
        founder_name: "Maria Santos",
        founder_background: "Former Goldman Sachs VP with 15 years in financial services. MBA from Wharton. Expert in SMB finance.",
        website: "https://financeflow.com",
        additional_info: "10,000+ SMB customers. $500K monthly recurring revenue. 95% customer retention."
      }
    }
  ]);

  // Load demo scenarios from API
  useEffect(() => {
    const loadDemoScenarios = async () => {
      try {
        const response = await fetch('/api/demo-scenarios');
        if (response.ok) {
          const data = await response.json();
          if (data.scenarios && data.scenarios.length > 0) {
            setDemoScenarios(data.scenarios.map((scenario: any, index: number) => ({
              id: `scenario-${index}`,
              name: scenario.company_name,
              description: scenario.description,
              data: {
                company_name: scenario.company_name,
                business_description: scenario.description,
                industry: scenario.industry,
                stage: scenario.stage,
                founder_name: "Demo Founder",
                founder_background: "Experienced entrepreneur with relevant industry background",
                website: `https://${scenario.company_name.toLowerCase().replace(/\s+/g, '')}.com`,
                additional_info: scenario.key_metrics || "Strong early traction and growth metrics"
              }
            })));
          }
        }
      } catch (error) {
        console.error('Failed to load demo scenarios:', error);
      }
    };

    loadDemoScenarios();
  }, []);

  const handleAnalyze = async (startupInput: StartupInput) => {
    setIsAnalyzing(true);
    setError(null);
    setResults(null);
    setShowRealTimeProgress(true);

    // Generate startup ID for tracking
    const startupId = `${startupInput.company_name.replace(/\s+/g, '_')}_${Date.now()}`;
    setCurrentStartupId(startupId);

    try {
      // Add uploaded files information to the analysis
      const enhancedInput = {
        ...startupInput,
        uploaded_files: uploadedFiles.map(file => ({
          name: file.name,
          url: file.public_url,
          size: file.size,
          type: file.type || 'unknown'
        }))
      };

      const response = await analyzeStartup(enhancedInput);
      // Results will be set by the real-time progress component
    } catch (err: any) {
      setError(err.message || 'Analysis failed. Please try again.');
      setIsAnalyzing(false);
      setShowRealTimeProgress(false);
    }
  };

  const handleDemoScenario = (scenario: any) => {
    const startupInput: StartupInput = {
      company_name: scenario.data.company_name,
      business_description: scenario.data.business_description,
      industry: scenario.data.industry,
      stage: scenario.data.stage,
      founder_name: scenario.data.founder_name,
      founder_background: scenario.data.founder_background,
      website: scenario.data.website,
      additional_info: scenario.data.additional_info,
    };
    handleAnalyze(startupInput);
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
    setIsAnalyzing(false);
    setShowRealTimeProgress(false);
    setCurrentStartupId(null);
    setUploadedFiles([]);
  };

  const handleFileUploaded = (fileInfo: UploadedFile) => {
    setUploadedFiles(prev => [...prev, fileInfo]);
  };

  const handleAnalysisComplete = (analysisResults: any) => {
    setResults(analysisResults);
    setIsAnalyzing(false);
    setShowRealTimeProgress(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {!results && !isAnalyzing && !showRealTimeProgress && (
          <div className="space-y-8">
            <div className="text-center">
              <h1 className="text-4xl font-bold text-gray-900 mb-4">
                🚀 AI-Powered Startup Analysis
              </h1>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Comprehensive investment analysis powered by Google's advanced tech stack. 
                Our multi-agent AI system provides professional-grade insights with real-time collaboration.
              </p>
              
              {/* Google Tech Stack Badges */}
              <div className="flex flex-wrap justify-center gap-2 mt-4">
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  🔥 Firebase Real-time
                </span>
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  ☁️ Cloud Storage
                </span>
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                  🤖 Google ADK
                </span>
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                  🧠 Gemini AI
                </span>
              </div>
            </div>

            <DemoScenarios scenarios={demoScenarios} onSelectScenario={handleDemoScenario} />
            
            <div className="max-w-4xl mx-auto">
              <div className="bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h2 className="text-lg font-semibold text-gray-900">📋 Startup Analysis Form</h2>
                  <p className="text-sm text-gray-600 mt-1">
                    Provide startup information and optionally upload supporting documents
                  </p>
                </div>
                
                <div className="p-6 space-y-6">
                  {/* File Upload Section */}
                  <div>
                    <h3 className="text-sm font-medium text-gray-900 mb-3">📎 Supporting Documents (Optional)</h3>
                    <FileUpload 
                      onFileUploaded={handleFileUploaded}
                      startupId={currentStartupId || undefined}
                    />
                  </div>
                  
                  {/* Startup Form */}
                  <div>
                    <h3 className="text-sm font-medium text-gray-900 mb-3">ℹ️ Company Information</h3>
                    <StartupForm onSubmit={handleAnalyze} />
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Real-time Progress */}
        {showRealTimeProgress && currentStartupId && (
          <div className="max-w-4xl mx-auto">
            <RealTimeProgress 
              startupId={currentStartupId}
              onComplete={handleAnalysisComplete}
            />
          </div>
        )}

        {/* Loading Spinner (Fallback) */}
        {isAnalyzing && !showRealTimeProgress && (
          <div className="max-w-4xl mx-auto">
            <LoadingSpinner />
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="max-w-4xl mx-auto">
            <div className="bg-red-50 border border-red-200 rounded-lg p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">
                    Analysis Error
                  </h3>
                  <div className="mt-2 text-sm text-red-700">
                    <p>{error}</p>
                  </div>
                  <div className="mt-4">
                    <button
                      onClick={handleReset}
                      className="bg-red-100 px-3 py-2 rounded-md text-sm font-medium text-red-800 hover:bg-red-200"
                    >
                      Try Again
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Analysis Results */}
        {results && (
          <div className="max-w-6xl mx-auto">
            <div className="mb-6">
              <div className="bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-lg p-4">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-green-800">
                      🎉 Analysis Complete!
                    </h3>
                    <div className="mt-1 text-sm text-green-700">
                      <p>Professional investment analysis generated using Google's comprehensive tech stack</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <AnalysisResults results={results} onReset={handleReset} />
          </div>
        )}
      </main>

      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-gray-500">
            <p className="font-medium">Powered by Google Tech Stack</p>
            <div className="flex justify-center space-x-4 mt-2 text-xs">
              <span>🔥 Firebase</span>
              <span>☁️ Cloud Storage</span>
              <span>🤖 Google ADK</span>
              <span>🧠 Gemini AI</span>
              <span>⚡ Real-time</span>
            </div>
            <p className="mt-2 text-sm">
              Professional startup investment analysis platform with real-time collaboration
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default AppEnhanced;
