export interface StartupInput {
  company_name: string;
  business_description: string;
  industry?: string;
  stage?: string;
  founder_name?: string;
  founder_background?: string;
  website?: string;
  pitch_deck_url?: string;
  additional_info?: string;
  pdf_content?: any; // Extracted PDF content
  uploaded_files?: {
    name: string;
    url: string;
    size: number;
    type: string;
  }[];
}

export interface MarketAnalysis {
  market_size?: string;
  growth_rate?: string;
  competition_level?: string;
  market_trends?: string;
  target_customers?: string;
}

export interface BusinessModelAnalysis {
  revenue_model?: string;
  scalability?: string;
  competitive_advantage?: string;
  monetization_strategy?: string;
  unit_economics?: string;
}

export interface RiskAssessment {
  market_risk: 'LOW' | 'MEDIUM' | 'HIGH';
  technology_risk: 'LOW' | 'MEDIUM' | 'HIGH';
  financial_risk: 'LOW' | 'MEDIUM' | 'HIGH';
  team_risk: 'LOW' | 'MEDIUM' | 'HIGH';
  regulatory_risk: 'LOW' | 'MEDIUM' | 'HIGH';
  risk_summary: string;
  mitigation_strategies: string[];
}

export interface InvestmentInsights {
  recommendation: 'INVEST' | 'PASS' | 'WATCH';
  confidence_score: number;
  key_thesis: string[];
  valuation_considerations?: string;
  due_diligence_priorities: string[];
  exit_potential?: string;
}

export interface AnalysisResults {
  startup_input: StartupInput;
  market_analysis: MarketAnalysis;
  business_model_analysis: BusinessModelAnalysis;
  risk_assessment: RiskAssessment;
  investment_insights: InvestmentInsights;
  analysis_timestamp: string;
  processing_time: number;
  agent_results: Record<string, any>;
}

export interface ApiResponse<T> {
  status: string;
  results?: T;
  startup_id?: string;
  timestamp: string;
}
