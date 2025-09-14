# AI-Powered Startup Analyst Platform

## 🚀 Hackathon Project Overview

An AI-powered analyst platform that evaluates startups by synthesizing founder materials and public data to generate concise, actionable investment insights using **Google's complete agentic AI framework**.

## 🎯 Key Features

- **Multi-Agent Analysis**: Specialized AI agents built with Vertex AI Agent Builder
- **Real-time Collaboration**: Firebase Studio for live updates and team collaboration
- **Advanced AI Orchestration**: Google ADK for complex multi-agent workflows
- **Investment Insights**: Generates actionable investment recommendations using Gemini API
- **Enterprise-Grade**: Built entirely on Google Cloud Platform with production-ready architecture

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Firebase      │    │   Vertex AI      │    │   Google AI     │
│   Studio        │◄──►│   Agent Builder  │◄──►│   SDK + Gemini  │
│   (Frontend)    │    │   + ADK          │    │   (Backend)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Firebase       │
                    │   Firestore      │
                    │   (Data Store)   │
                    └──────────────────┘
```

## 🤖 AI Agents (Built with Vertex AI Agent Builder)

1. **Data Collection Agent**: Gathers founder materials and public data using Gemini API
2. **Business Analysis Agent**: Analyzes business model, market, and team with specialized prompts
3. **Risk Assessment Agent**: Evaluates potential risks and challenges with advanced reasoning
4. **Investment Insights Agent**: Generates actionable recommendations using Google AI SDK
5. **Report Generation Agent**: Creates comprehensive analysis reports with real-time collaboration

## 🛠️ Google Tech Stack

- **AI Framework**: Vertex AI Agent Builder + Google ADK
- **AI Models**: Gemini API with Google AI SDK
- **Frontend**: Firebase Studio with real-time updates
- **Backend**: Google Cloud Functions + Vertex AI
- **Data Storage**: Firebase Firestore
- **Orchestration**: Google ADK for multi-agent workflows
- **Deployment**: Google Cloud Run

## 📋 Requirements

```bash
pip install -r requirements_google_stack.txt
```

## 🚀 Quick Start

1. **Set up Google Cloud Project**
   ```bash
   gcloud projects create startup-analyst-platform
   gcloud config set project startup-analyst-platform
   ```

2. **Enable Required APIs**
   ```bash
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable firestore.googleapis.com
   gcloud services enable run.googleapis.com
   ```

3. **Configure Environment**
   ```bash
   export GOOGLE_CLOUD_PROJECT="startup-analyst-platform"
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"
   ```

4. **Run Demo**
   ```bash
   streamlit run app.py
   ```

## 📊 Sample Output

The platform generates:
- **Executive Summary**: Key findings and recommendations
- **Market Analysis**: Market size, competition, trends
- **Team Assessment**: Founder experience and capabilities
- **Financial Projections**: Revenue models and growth potential
- **Risk Analysis**: Potential challenges and mitigation strategies
- **Investment Recommendation**: Go/No-go decision with reasoning

## 🎯 Hackathon Deliverables

- ✅ Working prototype with Google agentic AI
- ✅ Multi-agent system for startup analysis
- ✅ Real-time data synthesis and insights
- ✅ Professional web interface
- ✅ Deployed on Google Cloud Platform
