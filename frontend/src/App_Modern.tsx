import React, { useState } from 'react';
import { PlayIcon } from '@heroicons/react/24/solid';
import { CheckCircleIcon, StarIcon } from '@heroicons/react/24/outline';
import MultiModalUpload from './components/MultiModalUpload';
import RealTimeProgress from './components/RealTimeProgress';
import ModernResults from './components/ModernResults';
import { analyzeStartup } from './services/api';
import { analyzeStartupDemo, uploadFileDemo } from './services/demoApi';
import { StartupInput, AnalysisResults as AnalysisResultsType } from './types';

interface UploadedFile {
  name: string;
  size: number;
  type: 'document' | 'audio' | 'video' | 'questionnaire';
  public_url?: string;
  storage_path?: string;
  timestamp: number;
  processing_status?: 'pending' | 'processing' | 'completed' | 'failed';
}

const AppModern: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<'landing' | 'upload' | 'analysis' | 'progress' | 'results'>('landing');
  const [results, setResults] = useState<AnalysisResultsType | null>(null);
  const [currentStartupId, setCurrentStartupId] = useState<string | null>(null);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [startupInfo, setStartupInfo] = useState({
    company_name: '',
    industry: '',
    stage: '',
    description: '',
    founder_name: '',
    funding_request: ''
  });

  const testimonials = [
    {
      text: "I am still gasping at the depth, the detailing, the thought process and the application of this AI. Just unbelievable!",
      author: "Harish S.",
      role: "Learning & Development Leader"
    },
    {
      text: "The multi-modal analysis completely transformed our investment process. Professional grade insights in minutes.",
      author: "Sarah Chen",
      role: "Venture Capital Partner"
    },
    {
      text: "Revolutionary platform for startup analysis. The deal memos are investment committee ready.",
      author: "Michael Rodriguez",
      role: "Angel Investor"
    }
  ];


  const handleStartAnalysis = () => {
    setCurrentStep('upload');
  };

  const handleFilesUploaded = (files: UploadedFile[]) => {
    setUploadedFiles(files);
  };

  const handleStartupInfoChange = (field: string, value: string) => {
    setStartupInfo(prev => ({ ...prev, [field]: value }));
  };

  const handleBeginAnalysis = async () => {
    // Company info is optional for demo - use defaults if not provided
    const companyName = startupInfo.company_name || 'Demo Company';
    const description = startupInfo.description || 'Demo startup for hackathon presentation';

    // Show loading state
    setCurrentStep('analysis');

    try {
      const enhancedInput: StartupInput = {
        company_name: companyName,
        business_description: description,
        industry: startupInfo.industry || 'Technology',
        stage: startupInfo.stage || 'Seed',
        founder_name: startupInfo.founder_name || 'Demo Founder',
        founder_background: "Experienced entrepreneur",
        website: `https://${companyName.toLowerCase().replace(/\s+/g, '')}.com`,
        additional_info: `Funding request: ${startupInfo.funding_request || 'TBD'}`,
        pdf_content: uploadedFiles.length > 0 ? { demo: true } : null,
        uploaded_files: uploadedFiles.map(file => ({
          name: file.name,
          url: file.public_url || '',
          size: file.size,
          type: file.type || 'unknown'
        }))
      };

      console.log('Starting analysis for:', companyName);
      // Use demo API for Vercel deployment
      const response = { results: await analyzeStartupDemo(enhancedInput) };
      console.log('Analysis response:', response);
      
      if (response && response.results) {
        console.log('✅ Analysis successful, setting results');
        setResults(response.results);
        setCurrentStep('results');
        
        // Force immediate re-render
        setTimeout(() => {
          console.log('Force refresh completed');
        }, 100);
      } else {
        throw new Error('No results received from analysis');
      }
    } catch (error: any) {
      console.error('Analysis error:', error);
      alert(`Analysis failed: ${error.message}. Please try again.`);
      setCurrentStep('upload');
    }
  };

  const handleReset = () => {
    setCurrentStep('landing');
    setResults(null);
    setUploadedFiles([]);
    setStartupInfo({
      company_name: '',
      industry: '',
      stage: '',
      description: '',
      founder_name: '',
      funding_request: ''
    });
    setCurrentStartupId(null);
  };

  // Debug current step
  console.log('Current step:', currentStep);
  console.log('Results available:', !!results);

  return (
    <div className="min-h-screen bg-white">
      {/* Landing Page */}
      {currentStep === 'landing' && (
        <>
          {/* Header */}
          <header className="px-6 py-6 bg-white">
            <div className="max-w-7xl mx-auto flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">SA</span>
                </div>
                <span className="text-2xl font-bold text-gray-900">StartupAnalyst</span>
              </div>
              
              <nav className="hidden md:flex items-center space-x-8">
                <button className="text-gray-600 hover:text-gray-900 font-medium">Features</button>
                <button className="text-gray-600 hover:text-gray-900 font-medium">Pricing</button>
                <button className="text-gray-600 hover:text-gray-900 font-medium">Community</button>
                <button className="bg-green-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-green-700 transition-colors">
                  Live Demo
                </button>
              </nav>
            </div>
          </header>

          {/* Hero Section */}
          <main className="px-6 py-16 bg-white">
            <div className="max-w-7xl mx-auto bg-white">
              <div className="text-center mb-16">
                {/* Badge */}
                <div className="inline-flex items-center px-4 py-2 bg-green-100 text-green-800 rounded-full text-sm font-medium mb-8">
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                  Multi-Modal AI Analysis • Google Tech Stack • Real-time Insights
                </div>

                {/* Main Headline */}
                <h1 className="text-6xl md:text-7xl font-bold text-gray-900 mb-6 leading-tight">
                  <span className="text-green-600">All-in-One</span> solution
                  <br />
                  <span className="text-gray-900">for your startup</span>
                </h1>

                {/* Subtitle */}
                <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
                  Revolutionize Your Investment Decisions with AI-Powered Analysis.
                </p>
                {/* Feature Highlights */}
                <div className="flex flex-col md:flex-row items-center justify-center space-y-4 md:space-y-0 md:space-x-8 mb-12">
                  <div className="flex items-center space-x-2 text-green-700">
                    <CheckCircleIcon className="w-5 h-5" />
                    <span className="font-semibold">AI-Powered Multi-Modal Analysis</span>
                  </div>
                  <div className="flex items-center space-x-2 text-green-700">
                    <CheckCircleIcon className="w-5 h-5" />
                    <span className="font-semibold">Real-time Insights & Scoring</span>
                  </div>
                  <div className="flex items-center space-x-2 text-green-700">
                    <CheckCircleIcon className="w-5 h-5" />
                    <span className="font-semibold">Human Judgment Integration</span>
                  </div>
                </div>
                
                <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
                  Preserving the "people business" of VC while leveraging AI for comprehensive analysis
                </p>
                {/* CTA Buttons */}
                <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4 mb-4">
                  <button 
                    onClick={handleStartAnalysis}
                    className="bg-green-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-green-700 transition-all duration-200 flex items-center space-x-2 shadow-lg hover:shadow-xl"
                  >
                    <span>Start Analysis</span>
                    <PlayIcon className="w-5 h-5" />
                  </button>
                  <button className="border border-gray-300 text-gray-700 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-gray-50 transition-colors">
                    Watch Demo
                  </button>
                </div>

                <p className="text-sm text-gray-500 flex items-center justify-center">
                  <CheckCircleIcon className="w-4 h-4 mr-1" />
                  No credit card required
                </p>
              </div>


              {/* Tech Stack Badges */}
              <div className="text-center mb-16">
                <p className="text-sm text-gray-500 mb-4">Powered by Google's Advanced Tech Stack</p>
                <div className="flex flex-wrap justify-center gap-3">
                  {['🔥 Firebase', '☁️ Cloud Storage', '🤖 Vertex AI', '🧠 Gemini', '📊 Real-time'].map(tech => (
                    <span key={tech} className="bg-gray-100 text-gray-700 px-4 py-2 rounded-full text-sm font-medium">
                      {tech}
                    </span>
                  ))}
                </div>
              </div>

              {/* Testimonials */}
              <div className="grid md:grid-cols-3 gap-8">
                {testimonials.map((testimonial, index) => (
                  <div key={index} className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
                    <div className="flex mb-4">
                      {[...Array(5)].map((_, i) => (
                        <StarIcon key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                      ))}
                    </div>
                    <p className="text-gray-600 mb-4 italic">"{testimonial.text}"</p>
                    <div>
                      <p className="font-semibold text-gray-900">{testimonial.author}</p>
                      <p className="text-sm text-gray-500">{testimonial.role}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </main>
        </>
      )}

      {/* Upload Page */}
      {currentStep === 'upload' && (
        <div className="min-h-screen bg-white">
          <header className="px-6 py-6 border-b border-gray-200">
            <div className="max-w-4xl mx-auto flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">SA</span>
                </div>
                <span className="text-xl font-bold text-gray-900">StartupAnalyst</span>
              </div>
              <button 
                onClick={handleReset}
                className="text-gray-600 hover:text-gray-900"
              >
                ← Back to Home
              </button>
            </div>
          </header>

          <main className="px-6 py-12">
            <div className="max-w-4xl mx-auto">
              <div className="text-center mb-12">
                <h1 className="text-4xl font-bold text-gray-900 mb-4">
                  Upload Your Pitch Deck
                </h1>
                <p className="text-xl text-gray-600 mb-4">
                  Upload your pitch deck for AI-powered investment analysis
                </p>
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-2xl mx-auto">
                  <p className="text-sm text-blue-800">
                    <strong>🎯 Primary Analysis Source:</strong> Your pitch deck contains the key information for investment decisions - business model, market opportunity, financial projections, and team details.
                  </p>
                </div>
              </div>

              {/* Progress Steps */}
              <div className="flex items-center justify-center mb-12">
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center text-sm font-medium">1</div>
                    <span className="text-green-600 font-medium">Upload</span>
                  </div>
                  <div className="w-16 h-0.5 bg-gray-200"></div>
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 bg-gray-200 text-gray-400 rounded-full flex items-center justify-center text-sm font-medium">2</div>
                    <span className="text-gray-400">Analysis</span>
                  </div>
                  <div className="w-16 h-0.5 bg-gray-200"></div>
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 bg-gray-200 text-gray-400 rounded-full flex items-center justify-center text-sm font-medium">3</div>
                    <span className="text-gray-400">Results</span>
                  </div>
                </div>
              </div>

              {/* Upload Section */}
              <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden mb-8">
                <div className="p-8">
                  <MultiModalUpload 
                    onFilesUploaded={handleFilesUploaded}
                    startupId={currentStartupId || undefined}
                  />
                </div>
              </div>

              {/* Startup Info Form */}
              <div className="bg-white rounded-2xl border border-gray-200 p-8 mb-8">
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Company Metadata</h3>
                <p className="text-sm text-gray-600 mb-4">
                  Optional supplementary information - Primary analysis is based on your pitch deck content
                </p>
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-3 mb-6">
                  <p className="text-xs text-gray-600">
                    <strong>Note:</strong> Investment decisions are primarily driven by pitch deck analysis. This form provides additional context but is not required for comprehensive analysis.
                  </p>
                </div>
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Company Name</label>
                    <input
                      type="text"
                      value={startupInfo.company_name}
                      onChange={(e) => handleStartupInfoChange('company_name', e.target.value)}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      placeholder="Enter company name"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Industry</label>
                    <input
                      type="text"
                      value={startupInfo.industry}
                      onChange={(e) => handleStartupInfoChange('industry', e.target.value)}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      placeholder="e.g., Healthcare AI, FinTech"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Stage</label>
                    <select
                      value={startupInfo.stage}
                      onChange={(e) => handleStartupInfoChange('stage', e.target.value)}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    >
                      <option value="">Select stage</option>
                      <option value="Pre-Seed">Pre-Seed</option>
                      <option value="Seed">Seed</option>
                      <option value="Series A">Series A</option>
                      <option value="Series B">Series B</option>
                      <option value="Series C+">Series C+</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Funding Request</label>
                    <input
                      type="text"
                      value={startupInfo.funding_request}
                      onChange={(e) => handleStartupInfoChange('funding_request', e.target.value)}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      placeholder="e.g., $5M"
                    />
                  </div>
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Company Description</label>
                    <textarea
                      value={startupInfo.description}
                      onChange={(e) => handleStartupInfoChange('description', e.target.value)}
                      rows={4}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      placeholder="Describe your company, product, and value proposition..."
                    />
                  </div>
                </div>
              </div>

              {/* Start Analysis Button */}
              <div className="text-center">
                <button
                  onClick={handleBeginAnalysis}
                  className="bg-green-600 text-white px-12 py-4 rounded-xl font-semibold text-lg hover:bg-green-700 transition-colors shadow-lg hover:shadow-xl"
                >
                  Begin AI Analysis
                </button>
                <p className="text-sm text-gray-500 mt-4">
                  Analysis typically takes 2-3 seconds • Driven by pitch deck content
                </p>
                {uploadedFiles.length > 0 && (
                  <p className="text-sm text-green-600 mt-2">
                    ✅ {uploadedFiles.length} file(s) uploaded and ready for analysis
                  </p>
                )}
              </div>
            </div>
          </main>
        </div>
      )}

      {/* Analysis Page */}
      {currentStep === 'analysis' && (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-6">
          <div className="max-w-2xl w-full text-center">
            <div className="bg-white rounded-2xl p-12 shadow-lg">
              <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-green-600 mx-auto mb-6"></div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Analyzing Your Startup
              </h2>
              <p className="text-gray-600 mb-6">
                Our AI agents are processing your pitch materials and generating insights...
              </p>
              <div className="space-y-3 text-sm text-gray-600">
                <div className="flex items-center justify-center space-x-3">
                  <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
                  <span className="font-medium">Data Extraction Agent</span>
                  <span className="text-gray-500">Processing pitch deck content...</span>
                </div>
                <div className="flex items-center justify-center space-x-3">
                  <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" style={{animationDelay: '0.4s'}}></div>
                  <span className="font-medium">Business Analysis & Mapping Agent</span>
                  <span className="text-gray-500">Evaluating business model...</span>
                </div>
                <div className="flex items-center justify-center space-x-3">
                  <div className="w-3 h-3 bg-orange-500 rounded-full animate-pulse" style={{animationDelay: '0.8s'}}></div>
                  <span className="font-medium">Risk Assessment Agent</span>
                  <span className="text-gray-500">Analyzing potential risks...</span>
                </div>
                <div className="flex items-center justify-center space-x-3">
                  <div className="w-3 h-3 bg-purple-500 rounded-full animate-pulse" style={{animationDelay: '1.2s'}}></div>
                  <span className="font-medium">Scheduling & Interview Agent</span>
                  <span className="text-gray-500">Preparing post-analysis interview system...</span>
                </div>
                <div className="flex items-center justify-center space-x-3">
                  <div className="w-3 h-3 bg-indigo-500 rounded-full animate-pulse" style={{animationDelay: '1.6s'}}></div>
                  <span className="font-medium">Refinement & Investment Insights Agent</span>
                  <span className="text-gray-500">Generating final recommendations...</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Results Page */}
      {currentStep === 'results' && results && (
        <div className="min-h-screen bg-white">
          <header className="px-6 py-6 border-b border-gray-200">
            <div className="max-w-6xl mx-auto flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">SA</span>
                </div>
                <span className="text-xl font-bold text-gray-900">StartupAnalyst</span>
              </div>
              <div className="flex items-center space-x-4">
                <button 
                  onClick={handleReset}
                  className="text-gray-600 hover:text-gray-900 px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-50"
                >
                  New Analysis
                </button>
                <button className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700">
                  Export Report
                </button>
              </div>
            </div>
          </header>

          <main className="px-6 py-12">
            <div className="max-w-6xl mx-auto">
              <ModernResults results={results} onReset={handleReset} />
            </div>
          </main>
        </div>
      )}
    </div>
  );
};

export default AppModern;
