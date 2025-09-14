import React, { useState, useEffect } from 'react';
import { PlayIcon, DocumentTextIcon, MicrophoneIcon, VideoCameraIcon } from '@heroicons/react/24/solid';
import { CheckCircleIcon, StarIcon } from '@heroicons/react/24/outline';
import MultiModalUpload from './components/MultiModalUpload';
import RealTimeProgress from './components/RealTimeProgress';
import ModernResults from './components/ModernResults';
import { analyzeStartup } from './services/api';
import { StartupInput, AnalysisResults as AnalysisResultsType } from './types';

interface UploadedFile {
  name: string;
  size: number;
  type: 'document' | 'audio' | 'video';
  public_url?: string;
  storage_path?: string;
  timestamp: number;
  processing_status?: 'pending' | 'processing' | 'completed' | 'failed';
}

const AppModern: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<'landing' | 'upload' | 'analysis' | 'results'>('landing');
  const [results, setResults] = useState<AnalysisResultsType | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
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

  const features = [
    {
      icon: DocumentTextIcon,
      title: "Pitch Deck Analysis",
      description: "Extract structured insights from presentations and documents"
    },
    {
      icon: MicrophoneIcon,
      title: "Voice Pitch Processing",
      description: "Analyze founder presentations and speaking quality"
    },
    {
      icon: VideoCameraIcon,
      title: "Video Pitch Analysis",
      description: "Comprehensive video analysis with speaker assessment"
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
    if (!startupInfo.company_name || !startupInfo.description) {
      alert('Please fill in company name and description');
      return;
    }

    setCurrentStep('analysis');
    setIsAnalyzing(true);

    const startupId = `${startupInfo.company_name.replace(/\s+/g, '_')}_${Date.now()}`;
    setCurrentStartupId(startupId);

    try {
      const enhancedInput: StartupInput = {
        company_name: startupInfo.company_name,
        business_description: startupInfo.description,
        industry: startupInfo.industry,
        stage: startupInfo.stage,
        founder_name: startupInfo.founder_name,
        founder_background: "Experienced entrepreneur",
        website: `https://${startupInfo.company_name.toLowerCase().replace(/\s+/g, '')}.com`,
        additional_info: `Funding request: ${startupInfo.funding_request}`,
        uploaded_files: uploadedFiles.map(file => ({
          name: file.name,
          url: file.public_url || '',
          size: file.size,
          type: file.type || 'unknown'
        }))
      };

      const response = await analyzeStartup(enhancedInput);
      setResults(response.results || null);
      setCurrentStep('results');
    } catch (error: any) {
      alert(`Analysis failed: ${error.message}`);
      setCurrentStep('upload');
    } finally {
      setIsAnalyzing(false);
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100">
      {/* Landing Page */}
      {currentStep === 'landing' && (
        <>
          {/* Header */}
          <header className="px-6 py-6">
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
          <main className="px-6 py-16">
            <div className="max-w-7xl mx-auto">
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

              {/* Features Grid */}
              <div className="grid md:grid-cols-3 gap-8 mb-16">
                {features.map((feature, index) => (
                  <div key={index} className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100 hover:shadow-lg transition-shadow">
                    <feature.icon className="w-12 h-12 text-green-600 mb-4" />
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">{feature.title}</h3>
                    <p className="text-gray-600">{feature.description}</p>
                  </div>
                ))}
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
                  Upload Your Pitch Materials
                </h1>
                <p className="text-xl text-gray-600">
                  Upload your pitch deck, voice notes, or video presentations for comprehensive AI analysis
                </p>
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
                <h3 className="text-xl font-semibold text-gray-900 mb-6">Company Information</h3>
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Company Name *</label>
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
                    <label className="block text-sm font-medium text-gray-700 mb-2">Company Description *</label>
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
                  disabled={!startupInfo.company_name || !startupInfo.description}
                  className="bg-green-600 text-white px-12 py-4 rounded-xl font-semibold text-lg hover:bg-green-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
                >
                  Begin AI Analysis
                </button>
                <p className="text-sm text-gray-500 mt-4">
                  Analysis typically takes 60-90 seconds
                </p>
              </div>
            </div>
          </main>
        </div>
      )}

      {/* Analysis Page */}
      {currentStep === 'analysis' && currentStartupId && (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-6">
          <div className="max-w-4xl w-full">
            <RealTimeProgress 
              startupId={currentStartupId}
              onComplete={(analysisResults) => {
                setResults(analysisResults);
                setCurrentStep('results');
              }}
            />
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
