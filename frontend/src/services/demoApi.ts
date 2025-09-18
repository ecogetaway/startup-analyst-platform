import { StartupInput, AnalysisResults } from '../types';

// Demo analysis templates based on industry
const DEMO_TEMPLATES = {
  'Technology': {
    recommendation: 'INVEST',
    confidence_score: 0.85,
    summary: 'Strong technology foundation with scalable AI/ML solution. Experienced team with proven track record in enterprise software. Clear path to market with existing customer validation.',
    key_strengths: [
      'Innovative AI-powered analytics platform',
      'Experienced founding team with domain expertise',
      'Strong early customer traction and validation',
      'Scalable technology architecture',
      'Clear monetization strategy'
    ],
    risk_factors: [
      'Competitive landscape with established players',
      'Need for significant customer acquisition investment',
      'Technology complexity may require extended development cycles'
    ]
  },
  'Healthcare': {
    recommendation: 'INVEST',
    confidence_score: 0.82,
    summary: 'Promising healthcare innovation addressing significant market need. Regulatory pathway clear with strong clinical validation approach.',
    key_strengths: [
      'Addresses critical healthcare challenge',
      'Strong clinical validation approach',
      'Experienced healthcare team',
      'Clear regulatory pathway',
      'Large addressable market'
    ],
    risk_factors: [
      'Regulatory approval timeline uncertainty',
      'High capital requirements for clinical trials',
      'Reimbursement landscape complexity'
    ]
  },
  'Fintech': {
    recommendation: 'INVEST',
    confidence_score: 0.88,
    summary: 'Innovative financial technology solution with strong market demand. Regulatory compliance framework well-established.',
    key_strengths: [
      'Disruptive fintech solution',
      'Strong regulatory compliance',
      'Experienced financial services team',
      'Growing market demand',
      'Clear revenue model'
    ],
    risk_factors: [
      'Regulatory environment complexity',
      'Established financial institution competition',
      'Customer acquisition costs in financial services'
    ]
  },
  'E-commerce': {
    recommendation: 'WATCH',
    confidence_score: 0.75,
    summary: 'Solid e-commerce platform with differentiated approach. Market validation strong but competitive landscape challenging.',
    key_strengths: [
      'Unique value proposition in crowded market',
      'Strong user engagement metrics',
      'Scalable platform architecture',
      'Clear customer acquisition strategy'
    ],
    risk_factors: [
      'Highly competitive e-commerce landscape',
      'Customer acquisition cost challenges',
      'Market saturation concerns'
    ]
  },
  'Education': {
    recommendation: 'INVEST',
    confidence_score: 0.80,
    summary: 'EdTech solution addressing real learning challenges. Strong pedagogical foundation with measurable outcomes.',
    key_strengths: [
      'Evidence-based learning approach',
      'Strong educator and student feedback',
      'Scalable technology platform',
      'Clear impact metrics',
      'Growing EdTech market'
    ],
    risk_factors: [
      'Educational institution sales cycles',
      'Budget constraints in education sector',
      'Technology adoption barriers'
    ]
  }
};

// Simulate API delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const analyzeStartupDemo = async (startup_input: StartupInput): Promise<AnalysisResults> => {
  // Simulate analysis time
  await delay(2000);
  
  // Determine template based on industry or default to Technology
  const industry = startup_input.industry || 'Technology';
  const template = DEMO_TEMPLATES[industry as keyof typeof DEMO_TEMPLATES] || DEMO_TEMPLATES.Technology;
  
  // Check if pitch deck is provided
  const has_pitch_deck = !!(startup_input.pitch_deck_url || startup_input.uploaded_files?.length);
  
  // Adjust confidence if pitch deck is provided
  const adjusted_confidence = has_pitch_deck ? 
    Math.min(template.confidence_score + 0.05, 0.95) : 
    template.confidence_score;
  
  // Generate ML prediction
  const team_size = 8;
  const funding_total = 2500000;
  const market_size = 500000000;
  const growth_rate = 15;
  const product_readiness = 4;
  
  const success_probability = 0.75 + (team_size * 0.01) + (funding_total / 10000000 * 0.1);
  const final_success_probability = Math.min(success_probability, 0.95);
  
  const analysis_results: AnalysisResults = {
    startup_input: startup_input,
    analysis_timestamp: new Date().toISOString(),
    processing_time: 2.1,
    
    market_analysis: {
      market_size: '500M',
      growth_rate: '15%',
      competition_level: 'Medium',
      market_trends: 'Growing demand for AI-powered solutions',
      target_customers: 'Enterprise customers and SMBs'
    },
    
    business_model_analysis: {
      revenue_model: 'SaaS subscription with freemium tier',
      scalability: 'High - cloud-based platform',
      competitive_advantage: 'AI-driven analytics and automation',
      monetization_strategy: 'Monthly/annual subscriptions + premium features',
      unit_economics: 'Strong LTV/CAC ratio expected'
    },
    
    risk_assessment: {
      market_risk: 'MEDIUM' as const,
      technology_risk: 'LOW' as const,
      financial_risk: 'MEDIUM' as const,
      team_risk: 'LOW' as const,
      regulatory_risk: 'LOW' as const,
      risk_summary: template.risk_factors.join(', '),
      mitigation_strategies: [
        'Diversify customer base',
        'Build strong technical team',
        'Maintain adequate cash runway',
        'Monitor regulatory changes'
      ]
    },
    
    investment_insights: {
      recommendation: template.recommendation as 'INVEST' | 'PASS' | 'WATCH',
      confidence_score: adjusted_confidence,
      key_thesis: template.key_strengths,
      valuation_considerations: 'Revenue multiple approach based on SaaS comparables',
      due_diligence_priorities: [
        'Technical architecture review',
        'Customer reference calls',
        'Financial model validation',
        'Team background verification'
      ],
      exit_potential: 'Strategic acquisition or IPO potential'
    },
    
    agent_results: {
      data_extraction: {
        agent_name: 'Data Extraction Agent',
        analysis_type: 'data_extraction',
        findings: {
          extraction_source: has_pitch_deck ? 'pitch_deck' : 'company_metadata',
          content_processed: `Successfully extracted key information from ${startup_input.company_name} submission`,
          data_quality: has_pitch_deck ? 'High' : 'Standard',
          structured_data: {
            company_overview: true,
            financial_data: has_pitch_deck ? 'Extracted' : 'Limited',
            market_analysis: true,
            team_information: true
          }
        },
        confidence_score: has_pitch_deck ? 0.90 : 0.75,
        timestamp: new Date().toISOString()
      },
      
      business_analysis: {
        agent_name: 'Business Analysis & Mapping Agent',
        analysis_type: 'business_analysis',
        findings: {
          analysis: `Based on ${has_pitch_deck ? 'pitch deck analysis' : 'company metadata'}: ${template.summary}`,
          key_points: template.key_strengths,
          data_source: has_pitch_deck ? 'pitch_deck' : 'metadata'
        },
        confidence_score: template.confidence_score,
        timestamp: new Date().toISOString()
      },
      
      risk_assessment: {
        agent_name: 'Risk Assessment Agent',
        analysis_type: 'risk_assessment',
        findings: {
          risk_analysis: `Key risks for ${startup_input.company_name}: ` + template.risk_factors.join(', '),
          risk_levels: template.risk_factors
        },
        confidence_score: 0.85,
        timestamp: new Date().toISOString()
      },
      
      scheduling_interview: {
        agent_name: 'Scheduling & Interview Agent',
        analysis_type: 'scheduling_interview',
        findings: {
          workflow_stage: 'post_analysis_followup',
          interview_purpose: 'Investor requires additional details beyond initial analysis',
          scheduling_status: 'Ready to schedule when requested',
          interview_capabilities: [
            'Automated founder interview scheduling',
            'AI-powered question generation based on analysis gaps',
            'Real-time interview conduct via video/audio',
            'Structured data extraction from founder responses'
          ],
          typical_questions: [
            'Financial projections deep-dive',
            'Team expansion plans', 
            'Technology roadmap details',
            'Market penetration strategy'
          ],
          demo_note: 'This agent activates when investors need clarification post-analysis - Production version will conduct live AI interviews'
        },
        confidence_score: 0.80,
        timestamp: new Date().toISOString()
      },
      
      investment_insights: {
        agent_name: 'Refinement & Investment Insights Agent',
        analysis_type: 'investment_insights', 
        findings: {
          investment_insights: `Investment Recommendation: ${template.recommendation}\n\nAnalysis Source: ${has_pitch_deck ? 'Comprehensive pitch deck review' : 'Company metadata analysis'}\n\nRationale: ${template.summary}\n\nKey Investment Highlights:\n` + template.key_strengths.map(point => `• ${point}`).join('\n'),
          recommendation: template.recommendation,
          key_thesis: template.key_strengths,
          analysis_basis: has_pitch_deck ? 'pitch_deck_driven' : 'metadata_driven'
        },
        confidence_score: template.confidence_score,
        timestamp: new Date().toISOString()
      }
    }
  };
  
  return analysis_results;
};

export const uploadFileDemo = async (file: File): Promise<{status: string; public_url: string; filename: string; size: number; timestamp: number}> => {
  // Simulate upload time
  await delay(1000);
  
  return {
    status: 'success',
    public_url: `https://demo-storage.vercel.app/${file.name}`,
    filename: file.name,
    size: file.size,
    timestamp: Date.now()
  };
};
