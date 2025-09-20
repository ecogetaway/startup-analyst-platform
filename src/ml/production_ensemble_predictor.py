#!/usr/bin/env python3
"""
Production-Ready Startup Success Prediction with Ensemble Models
Enhanced version with real feature engineering and multiple ML models
"""

import pandas as pd
import numpy as np
import warnings
import logging
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, asdict
import joblib
import os
from datetime import datetime
import json

# ML Libraries
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.model_selection import GridSearchCV, train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler, RobustScaler
from sklearn.impute import KNNImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.pipeline import Pipeline

# XGBoost disabled for stability
XGBOOST_AVAILABLE = False

# Suppress warnings
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ProductionStartupFeatures:
    """Enhanced features for production ML model"""
    # Basic Company Info
    company_name: str = ""
    industry: str = "Technology"
    founded_year: int = 2020
    team_size: int = 5
    location: str = "Unknown"
    business_stage: str = "Seed"  # Pre-seed, Seed, Series A, etc.
    
    # Financial Features (extracted from PDFs)
    funding_total_usd: float = 0.0
    funding_rounds: int = 0
    current_revenue_usd: float = 0.0
    projected_revenue_y1: float = 0.0
    projected_revenue_y3: float = 0.0
    burn_rate_monthly: float = 0.0
    runway_months: float = 0.0
    gross_margin_percent: float = 0.0
    
    # Market Features
    market_size_billions: float = 0.0  # TAM
    addressable_market_billions: float = 0.0  # SAM
    market_growth_rate: float = 0.0
    competition_level: int = 3  # 1-5 scale
    competitive_advantage_score: float = 0.5  # 0-1 scale
    
    # Team Features
    founder_experience_years: float = 0.0
    team_technical_score: float = 0.5  # 0-1 scale
    team_business_score: float = 0.5  # 0-1 scale
    advisor_quality_score: float = 0.5  # 0-1 scale
    
    # Product Features
    product_readiness_score: float = 0.5  # 0-1 scale
    tech_differentiation_score: float = 0.5  # 0-1 scale
    user_traction_score: float = 0.0  # 0-1 scale
    product_market_fit_score: float = 0.0  # 0-1 scale
    
    # Business Model Features
    business_model_clarity: float = 0.5  # 0-1 scale
    revenue_model_strength: float = 0.5  # 0-1 scale
    scalability_score: float = 0.5  # 0-1 scale
    go_to_market_score: float = 0.5  # 0-1 scale
    
    # Risk Features
    market_risk_score: float = 0.5  # 0-1 scale (higher = more risk)
    technical_risk_score: float = 0.5  # 0-1 scale
    team_risk_score: float = 0.5  # 0-1 scale
    financial_risk_score: float = 0.5  # 0-1 scale
    regulatory_risk_score: float = 0.5  # 0-1 scale
    
    # External Features
    industry_trend_score: float = 0.5  # 0-1 scale
    economic_environment_score: float = 0.5  # 0-1 scale
    vc_funding_climate_score: float = 0.5  # 0-1 scale
    
    # Pitch Quality Features
    pitch_clarity_score: float = 0.5  # 0-1 scale
    financial_projections_realism: float = 0.5  # 0-1 scale
    presentation_quality_score: float = 0.5  # 0-1 scale

@dataclass
class ProductionPredictionResult:
    """Enhanced prediction result with confidence intervals"""
    success_probability: float  # 0-1
    success_category: str  # "High Potential", "Medium Potential", "Low Potential"
    confidence_interval: Tuple[float, float]  # (lower, upper)
    investment_recommendation: str  # "INVEST", "WATCH", "PASS"
    
    # Detailed Scores
    market_score: float  # 0-100
    team_score: float  # 0-100
    product_score: float  # 0-100
    business_model_score: float  # 0-100
    financial_score: float  # 0-100
    risk_score: float  # 0-100 (lower is better)
    
    # Feature Importance
    key_strengths: List[Tuple[str, float]]
    key_risks: List[Tuple[str, float]]
    improvement_areas: List[str]
    
    # Model Details
    model_confidence: float  # 0-1
    prediction_timestamp: str
    model_version: str
    feature_count: int

class ProductionEnsemblePredictor:
    """
    Production-ready ensemble ML model for startup success prediction
    Combines multiple algorithms for robust predictions with uncertainty quantification
    """
    
    def __init__(self, model_version: str = "2.0.0"):
        self.model_version = model_version
        self.models = {}
        self.ensemble_model = None
        self.feature_scaler = RobustScaler()
        self.label_encoders = {}
        self.feature_importance = {}
        self.is_trained = False
        self.feature_columns = []
        self.model_performance = {}
        
        # Initialize individual models with optimized parameters
        self.base_models = {
            'random_forest': RandomForestClassifier(
                n_estimators=300,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            ),
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                random_state=42
            ),
            'ada_boost': AdaBoostClassifier(
                n_estimators=100,
                learning_rate=1.0,
                random_state=42
            )
        }
        
        # XGBoost disabled for stability (can be enabled later)
        # Will use Random Forest + Gradient Boosting + AdaBoost ensemble
        
    def extract_features_from_data(self, startup_data: Dict[str, Any]) -> ProductionStartupFeatures:
        """
        Extract enhanced features from startup data with better defaults
        """
        features = ProductionStartupFeatures()
        
        # Basic company information
        features.company_name = startup_data.get('company_name', '')
        features.industry = startup_data.get('industry', 'Technology')
        features.founded_year = startup_data.get('founded_year', 2020)
        features.team_size = startup_data.get('team_size', 5)
        features.location = startup_data.get('location', 'Unknown')
        features.business_stage = startup_data.get('business_stage', 'Seed')
        
        # Financial features (enhanced extraction)
        features.funding_total_usd = startup_data.get('funding_total', 0.0)
        features.funding_rounds = startup_data.get('funding_rounds', 0)
        features.current_revenue_usd = startup_data.get('revenue', 0.0)
        features.projected_revenue_y1 = startup_data.get('projected_revenue_y1', features.current_revenue_usd * 2)
        features.projected_revenue_y3 = startup_data.get('projected_revenue_y3', features.current_revenue_usd * 5)
        features.burn_rate_monthly = startup_data.get('burn_rate', 50000.0)
        features.runway_months = startup_data.get('runway_months', 12.0)
        features.gross_margin_percent = startup_data.get('gross_margin', 70.0)
        
        # Market features
        features.market_size_billions = startup_data.get('market_size', 1.0)
        features.addressable_market_billions = startup_data.get('sam', features.market_size_billions * 0.1)
        features.market_growth_rate = startup_data.get('market_growth_rate', 10.0)
        features.competition_level = startup_data.get('competition_level', 3)
        features.competitive_advantage_score = startup_data.get('competitive_advantage', 0.5)
        
        # Team features (from PDF analysis or defaults)
        features.founder_experience_years = startup_data.get('founder_experience', 5.0)
        features.team_technical_score = startup_data.get('team_technical_score', 0.6)
        features.team_business_score = startup_data.get('team_business_score', 0.6)
        features.advisor_quality_score = startup_data.get('advisor_quality', 0.5)
        
        # Product features
        features.product_readiness_score = startup_data.get('product_readiness', 0.6)
        features.tech_differentiation_score = startup_data.get('tech_differentiation', 0.5)
        features.user_traction_score = startup_data.get('user_traction', 0.3)
        features.product_market_fit_score = startup_data.get('pmf_score', 0.4)
        
        # Business model features
        features.business_model_clarity = startup_data.get('business_model_clarity', 0.6)
        features.revenue_model_strength = startup_data.get('revenue_model_strength', 0.6)
        features.scalability_score = startup_data.get('scalability', 0.6)
        features.go_to_market_score = startup_data.get('gtm_score', 0.5)
        
        # Risk features (derived or provided)
        features.market_risk_score = startup_data.get('market_risk', 0.4)
        features.technical_risk_score = startup_data.get('tech_risk', 0.4)
        features.team_risk_score = startup_data.get('team_risk', 0.3)
        features.financial_risk_score = startup_data.get('financial_risk', 0.5)
        features.regulatory_risk_score = startup_data.get('regulatory_risk', 0.3)
        
        # External features
        features.industry_trend_score = startup_data.get('industry_trend', 0.6)
        features.economic_environment_score = startup_data.get('economic_environment', 0.5)
        features.vc_funding_climate_score = startup_data.get('vc_climate', 0.6)
        
        # Pitch quality features
        features.pitch_clarity_score = startup_data.get('pitch_clarity', 0.6)
        features.financial_projections_realism = startup_data.get('projections_realism', 0.6)
        features.presentation_quality_score = startup_data.get('presentation_quality', 0.6)
        
        return features
    
    def create_enhanced_training_data(self, n_samples: int = 2000) -> pd.DataFrame:
        """
        Create enhanced synthetic training data with realistic correlations
        """
        np.random.seed(42)
        
        data = []
        
        for i in range(n_samples):
            # Create correlated features for realistic data
            industry_trend = np.random.beta(2, 2)  # 0-1
            market_size = np.random.lognormal(0, 1) * industry_trend * 2  # Correlated with trend
            
            # Team quality affects many other factors
            team_quality = np.random.beta(2, 2)
            founder_experience = team_quality * 10 + np.random.normal(0, 2)
            
            # Market and product features
            competitive_advantage = np.random.beta(2, 2)
            product_readiness = team_quality * 0.7 + np.random.beta(1, 1) * 0.3
            
            # Financial features with correlations
            funding_total = np.random.lognormal(12, 2)  # ~$150K median
            revenue = funding_total * np.random.beta(1, 3) * 0.1
            burn_rate = funding_total * 0.05 * np.random.lognormal(0, 0.5)
            
            # Create success probability based on weighted factors
            success_factors = (
                team_quality * 0.25 +
                (market_size / 10) * 0.2 +
                competitive_advantage * 0.15 +
                product_readiness * 0.15 +
                industry_trend * 0.1 +
                min(revenue / 100000, 1) * 0.15
            )
            
            # Add noise and threshold
            success_prob = min(success_factors + np.random.normal(0, 0.1), 1)
            is_success = 1 if success_prob > 0.6 else 0
            
            sample = {
                'funding_total_usd': funding_total,
                'funding_rounds': max(1, int(np.random.poisson(2))),
                'team_size': max(1, int(np.random.poisson(8))),
                'founded_year': int(np.random.uniform(2015, 2023)),
                'current_revenue_usd': revenue,
                'projected_revenue_y1': revenue * np.random.uniform(1.5, 3),
                'projected_revenue_y3': revenue * np.random.uniform(3, 8),
                'burn_rate_monthly': burn_rate,
                'runway_months': funding_total / (burn_rate * 12) if burn_rate > 0 else 24,
                'gross_margin_percent': np.random.uniform(20, 80),
                
                'market_size_billions': market_size,
                'addressable_market_billions': market_size * np.random.uniform(0.05, 0.2),
                'market_growth_rate': np.random.uniform(-5, 25),
                'competition_level': int(np.random.uniform(1, 6)),
                'competitive_advantage_score': competitive_advantage,
                
                'founder_experience_years': max(0, founder_experience),
                'team_technical_score': team_quality * 0.8 + np.random.uniform(0, 0.2),
                'team_business_score': team_quality * 0.7 + np.random.uniform(0, 0.3),
                'advisor_quality_score': np.random.beta(2, 2),
                
                'product_readiness_score': product_readiness,
                'tech_differentiation_score': competitive_advantage * 0.8 + np.random.uniform(0, 0.2),
                'user_traction_score': np.random.beta(1, 3),
                'product_market_fit_score': success_prob * 0.7 + np.random.uniform(0, 0.3),
                
                'business_model_clarity': team_quality * 0.6 + np.random.uniform(0, 0.4),
                'revenue_model_strength': np.random.beta(2, 2),
                'scalability_score': industry_trend * 0.7 + np.random.uniform(0, 0.3),
                'go_to_market_score': team_quality * 0.5 + np.random.uniform(0, 0.5),
                
                'market_risk_score': 1 - industry_trend + np.random.normal(0, 0.1),
                'technical_risk_score': 1 - product_readiness + np.random.normal(0, 0.1),
                'team_risk_score': 1 - team_quality + np.random.normal(0, 0.1),
                'financial_risk_score': np.random.beta(2, 2),
                'regulatory_risk_score': np.random.beta(1, 3),
                
                'industry_trend_score': industry_trend,
                'economic_environment_score': np.random.beta(2, 2),
                'vc_funding_climate_score': np.random.beta(2, 2),
                
                'pitch_clarity_score': team_quality * 0.6 + np.random.uniform(0, 0.4),
                'financial_projections_realism': np.random.beta(2, 2),
                'presentation_quality_score': np.random.beta(2, 2),
                
                'is_success': is_success
            }
            
            # Clip all probability scores to [0, 1]
            for key in sample:
                if 'score' in key and key != 'is_success':
                    sample[key] = np.clip(sample[key], 0, 1)
            
            data.append(sample)
        
        df = pd.DataFrame(data)
        logger.info(f"✅ Created enhanced training dataset with {len(df)} samples")
        logger.info(f"📊 Success rate: {df['is_success'].mean():.2%}")
        
        return df
    
    def train_ensemble_model(self):
        """
        Train ensemble model with cross-validation and performance tracking
        """
        logger.info("🚀 Starting enhanced ensemble model training...")
        
        # Create training data
        df = self.create_enhanced_training_data()
        
        # Prepare features
        feature_columns = [col for col in df.columns if col != 'is_success']
        self.feature_columns = feature_columns
        X = df[feature_columns]
        y = df['is_success']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.feature_scaler.fit_transform(X_train)
        X_test_scaled = self.feature_scaler.transform(X_test)
        
        # Train individual models
        trained_models = []
        model_scores = {}
        
        for name, model in self.base_models.items():
            logger.info(f"📊 Training {name}...")
            
            # Train model
            model.fit(X_train_scaled, y_train)
            
            # Evaluate
            y_pred = model.predict(X_test_scaled)
            y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
            
            accuracy = accuracy_score(y_test, y_pred)
            auc_score = roc_auc_score(y_test, y_pred_proba)
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='accuracy')
            
            model_scores[name] = {
                'accuracy': accuracy,
                'auc': auc_score,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std()
            }
            
            logger.info(f"✅ {name}: Accuracy={accuracy:.3f}, AUC={auc_score:.3f}, CV={cv_scores.mean():.3f}±{cv_scores.std():.3f}")
            
            trained_models.append((name, model))
            self.models[name] = model
        
        # Create ensemble model
        ensemble_estimators = [(name, model) for name, model in trained_models]
        self.ensemble_model = VotingClassifier(
            estimators=ensemble_estimators,
            voting='soft'  # Use probability voting
        )
        
        # Train ensemble
        logger.info("🎯 Training ensemble model...")
        self.ensemble_model.fit(X_train_scaled, y_train)
        
        # Evaluate ensemble
        y_pred_ensemble = self.ensemble_model.predict(X_test_scaled)
        y_pred_proba_ensemble = self.ensemble_model.predict_proba(X_test_scaled)[:, 1]
        
        ensemble_accuracy = accuracy_score(y_test, y_pred_ensemble)
        ensemble_auc = roc_auc_score(y_test, y_pred_proba_ensemble)
        
        model_scores['ensemble'] = {
            'accuracy': ensemble_accuracy,
            'auc': ensemble_auc
        }
        
        logger.info(f"🏆 Ensemble: Accuracy={ensemble_accuracy:.3f}, AUC={ensemble_auc:.3f}")
        
        # Store performance metrics
        self.model_performance = model_scores
        self.is_trained = True
        
        # Calculate feature importance (from Random Forest)
        if 'random_forest' in self.models:
            rf_model = self.models['random_forest']
            self.feature_importance = dict(zip(feature_columns, rf_model.feature_importances_))
        
        logger.info("🎯 Enhanced ensemble model training completed!")
        return model_scores
    
    def predict_startup_success(self, startup_data: Dict[str, Any]) -> ProductionPredictionResult:
        """
        Generate comprehensive prediction with confidence intervals
        """
        if not self.is_trained:
            logger.info("🔄 Training model as it's not trained yet...")
            self.train_ensemble_model()
        
        # Extract features
        features = self.extract_features_from_data(startup_data)
        
        # Convert to DataFrame
        feature_dict = asdict(features)
        # Remove non-numeric fields
        numeric_features = {k: v for k, v in feature_dict.items() 
                          if k in self.feature_columns and isinstance(v, (int, float))}
        
        # Create DataFrame
        X = pd.DataFrame([numeric_features])
        
        # Handle missing columns
        for col in self.feature_columns:
            if col not in X.columns:
                X[col] = 0.0
        
        # Reorder columns to match training
        X = X[self.feature_columns]
        
        # Scale features
        X_scaled = self.feature_scaler.transform(X)
        
        # Get ensemble prediction
        success_probability = self.ensemble_model.predict_proba(X_scaled)[0, 1]
        
        # Get individual model predictions for confidence estimation
        individual_predictions = []
        for name, model in self.models.items():
            pred_proba = model.predict_proba(X_scaled)[0, 1]
            individual_predictions.append(pred_proba)
        
        # Calculate confidence interval (based on prediction variance)
        pred_std = np.std(individual_predictions)
        confidence_lower = max(0, success_probability - 1.96 * pred_std)
        confidence_upper = min(1, success_probability + 1.96 * pred_std)
        
        # Determine categories and recommendations
        if success_probability >= 0.7:
            success_category = "High Potential"
            investment_recommendation = "INVEST"
        elif success_probability >= 0.4:
            success_category = "Medium Potential" 
            investment_recommendation = "WATCH"
        else:
            success_category = "Low Potential"
            investment_recommendation = "PASS"
        
        # Calculate component scores
        market_score = self._calculate_market_score(features)
        team_score = self._calculate_team_score(features)
        product_score = self._calculate_product_score(features)
        business_model_score = self._calculate_business_model_score(features)
        financial_score = self._calculate_financial_score(features)
        risk_score = self._calculate_risk_score(features)
        
        # Get key factors
        key_strengths = self._get_key_strengths(features, X_scaled[0])
        key_risks = self._get_key_risks(features, X_scaled[0])
        improvement_areas = self._get_improvement_areas(features)
        
        # Calculate model confidence
        model_confidence = 1 - pred_std  # Higher variance = lower confidence
        
        return ProductionPredictionResult(
            success_probability=success_probability,
            success_category=success_category,
            confidence_interval=(confidence_lower, confidence_upper),
            investment_recommendation=investment_recommendation,
            market_score=market_score,
            team_score=team_score,
            product_score=product_score,
            business_model_score=business_model_score,
            financial_score=financial_score,
            risk_score=risk_score,
            key_strengths=key_strengths,
            key_risks=key_risks,
            improvement_areas=improvement_areas,
            model_confidence=model_confidence,
            prediction_timestamp=datetime.now().isoformat(),
            model_version=self.model_version,
            feature_count=len(self.feature_columns)
        )
    
    def _calculate_market_score(self, features: ProductionStartupFeatures) -> float:
        """Calculate market opportunity score (0-100)"""
        market_size_score = min(features.market_size_billions / 10, 1) * 30
        growth_score = min(features.market_growth_rate / 20, 1) * 25
        competition_score = (5 - features.competition_level) / 4 * 20
        advantage_score = features.competitive_advantage_score * 25
        
        return market_size_score + growth_score + competition_score + advantage_score
    
    def _calculate_team_score(self, features: ProductionStartupFeatures) -> float:
        """Calculate team quality score (0-100)"""
        experience_score = min(features.founder_experience_years / 10, 1) * 30
        technical_score = features.team_technical_score * 25
        business_score = features.team_business_score * 25
        advisor_score = features.advisor_quality_score * 20
        
        return experience_score + technical_score + business_score + advisor_score
    
    def _calculate_product_score(self, features: ProductionStartupFeatures) -> float:
        """Calculate product strength score (0-100)"""
        readiness_score = features.product_readiness_score * 30
        differentiation_score = features.tech_differentiation_score * 25
        traction_score = features.user_traction_score * 25
        pmf_score = features.product_market_fit_score * 20
        
        return readiness_score + differentiation_score + traction_score + pmf_score
    
    def _calculate_business_model_score(self, features: ProductionStartupFeatures) -> float:
        """Calculate business model strength score (0-100)"""
        clarity_score = features.business_model_clarity * 25
        revenue_score = features.revenue_model_strength * 25
        scalability_score = features.scalability_score * 25
        gtm_score = features.go_to_market_score * 25
        
        return clarity_score + revenue_score + scalability_score + gtm_score
    
    def _calculate_financial_score(self, features: ProductionStartupFeatures) -> float:
        """Calculate financial health score (0-100)"""
        revenue_score = min(features.current_revenue_usd / 1000000, 1) * 25
        growth_score = min((features.projected_revenue_y1 / max(features.current_revenue_usd, 1)) / 3, 1) * 25
        runway_score = min(features.runway_months / 24, 1) * 25
        margin_score = features.gross_margin_percent / 100 * 25
        
        return revenue_score + growth_score + runway_score + margin_score
    
    def _calculate_risk_score(self, features: ProductionStartupFeatures) -> float:
        """Calculate overall risk score (0-100, lower is better)"""
        market_risk = features.market_risk_score * 20
        tech_risk = features.technical_risk_score * 20
        team_risk = features.team_risk_score * 20
        financial_risk = features.financial_risk_score * 20
        regulatory_risk = features.regulatory_risk_score * 20
        
        return (market_risk + tech_risk + team_risk + financial_risk + regulatory_risk) * 100
    
    def _get_key_strengths(self, features: ProductionStartupFeatures, X_scaled: np.ndarray) -> List[Tuple[str, float]]:
        """Identify key strengths based on feature importance and values"""
        strengths = []
        
        # Check high-value features
        if features.market_size_billions > 5:
            strengths.append(("Large market opportunity", features.market_size_billions))
        if features.team_technical_score > 0.7:
            strengths.append(("Strong technical team", features.team_technical_score))
        if features.competitive_advantage_score > 0.7:
            strengths.append(("Clear competitive advantage", features.competitive_advantage_score))
        if features.user_traction_score > 0.6:
            strengths.append(("Strong user traction", features.user_traction_score))
        
        return strengths[:3]  # Top 3 strengths
    
    def _get_key_risks(self, features: ProductionStartupFeatures, X_scaled: np.ndarray) -> List[Tuple[str, float]]:
        """Identify key risks based on feature values"""
        risks = []
        
        if features.market_risk_score > 0.6:
            risks.append(("High market risk", features.market_risk_score))
        if features.runway_months < 6:
            risks.append(("Short runway", features.runway_months))
        if features.competition_level >= 4:
            risks.append(("High competition", features.competition_level))
        if features.team_risk_score > 0.6:
            risks.append(("Team execution risk", features.team_risk_score))
        
        return risks[:3]  # Top 3 risks
    
    def _get_improvement_areas(self, features: ProductionStartupFeatures) -> List[str]:
        """Suggest improvement areas"""
        areas = []
        
        if features.user_traction_score < 0.4:
            areas.append("Increase user traction and engagement")
        if features.go_to_market_score < 0.5:
            areas.append("Strengthen go-to-market strategy")
        if features.runway_months < 12:
            areas.append("Extend financial runway")
        if features.team_business_score < 0.6:
            areas.append("Strengthen business expertise on team")
        
        return areas[:3]  # Top 3 improvement areas
    
    def save_model(self, filepath: str):
        """Save the trained model"""
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        model_data = {
            'ensemble_model': self.ensemble_model,
            'individual_models': self.models,
            'feature_scaler': self.feature_scaler,
            'feature_columns': self.feature_columns,
            'feature_importance': self.feature_importance,
            'model_performance': self.model_performance,
            'model_version': self.model_version
        }
        
        joblib.dump(model_data, filepath)
        logger.info(f"✅ Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load a trained model"""
        model_data = joblib.load(filepath)
        
        self.ensemble_model = model_data['ensemble_model']
        self.models = model_data['individual_models']
        self.feature_scaler = model_data['feature_scaler']
        self.feature_columns = model_data['feature_columns']
        self.feature_importance = model_data['feature_importance']
        self.model_performance = model_data['model_performance']
        self.model_version = model_data['model_version']
        self.is_trained = True
        
        logger.info(f"✅ Model loaded from {filepath}")

# Global predictor instance
_global_predictor = None

def get_production_predictor() -> ProductionEnsemblePredictor:
    """Get or create global predictor instance"""
    global _global_predictor
    if _global_predictor is None:
        _global_predictor = ProductionEnsemblePredictor()
    return _global_predictor

def predict_startup_success_production(startup_data: Dict[str, Any]) -> ProductionPredictionResult:
    """
    Main function for production startup success prediction
    """
    predictor = get_production_predictor()
    return predictor.predict_startup_success(startup_data)

if __name__ == "__main__":
    # Test the production predictor
    predictor = ProductionEnsemblePredictor()
    
    # Train model
    performance = predictor.train_ensemble_model()
    print("🎯 Model Performance:")
    for model, metrics in performance.items():
        print(f"  {model}: {metrics}")
    
    # Test prediction
    test_startup = {
        'company_name': 'TestStartup AI',
        'industry': 'Technology',
        'market_size': 5.0,
        'team_size': 8,
        'revenue': 500000,
        'founder_experience': 7,
        'product_readiness': 0.8,
        'competitive_advantage': 0.7
    }
    
    result = predictor.predict_startup_success(test_startup)
    print(f"\n🚀 Prediction for {test_startup['company_name']}:")
    print(f"  Success Probability: {result.success_probability:.1%}")
    print(f"  Recommendation: {result.investment_recommendation}")
    print(f"  Market Score: {result.market_score:.1f}/100")
    print(f"  Team Score: {result.team_score:.1f}/100")
    print(f"  Product Score: {result.product_score:.1f}/100")
