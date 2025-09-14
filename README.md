# 🚀 Startup Analyst Platform

Welcome to the **AI-Powered Startup Analyst Platform**! This project leverages the full Google Cloud and AI stack to provide comprehensive investment analysis for startups.

## 📚 Documentation

All project documentation, guides, and detailed explanations are now organized in the `documentation/` folder.

**Start here:**
- **[Documentation Index](documentation/DOCUMENTATION_INDEX.md)**: A comprehensive index of all available documentation.
- **[Quick Setup Guide](documentation/QUICK_SETUP_GUIDE.md)**: Step-by-step instructions to set up your Google Cloud environment.
- **[Comprehensive Google Stack Gap Analysis](documentation/COMPREHENSIVE_GOOGLE_STACK_GAP_ANALYSIS.md)**: Detailed plan for implementing the full Google tech stack.
- **[Implementation Roadmap](documentation/IMPLEMENTATION_ROADMAP.md)**: Priority queue and timeline for development.

## 🚀 Getting Started

To run the full-stack application locally:

1.  **Ensure Google Cloud setup is complete** as per the [Quick Setup Guide](documentation/QUICK_SETUP_GUIDE.md).
2.  **Install Python dependencies**: `pip install -r requirements.txt`
3.  **Install Node.js dependencies**: `cd frontend && npm install`
4.  **Start the application**: `./start.sh` (for the original frontend) or `./start_enhanced.sh` (for the enhanced frontend) or `./start_modern_demo.sh` (for the VenturusAI-inspired frontend).

**Access the application:**
- **Frontend**: `http://localhost:8080`
- **API Docs**: `http://localhost:8080/docs`

## ✨ Features

- **AI-Powered Analysis**: Leverage Google Gemini and Vertex AI for deep insights.
- **Multi-Agent System**: Specialized agents for data collection, business analysis, risk assessment, investment insights, and report generation.
- **Real-time Collaboration**: Firebase for live updates and data persistence.
- **Multi-Modal Pitch Ingestion**: Process pitch decks, voice notes, and video.
- **Structured Deal Memo Generation**: Automated investment memo creation.
- **Modern Frontend**: Responsive and intuitive user interface built with React and Tailwind CSS.
- **Scalable Backend**: FastAPI for high-performance API services.
- **Cloud Deployment**: Ready for deployment on Google Cloud Run.

## 🎯 Project Structure

```
startup-analyst-platform/
├── documentation/          # All project documentation
├── frontend/              # React + TypeScript frontend
├── backend/               # FastAPI backend
├── src/                   # Core Python modules
│   ├── agents/            # AI agent implementations
│   ├── config/            # Configuration settings
│   └── utils/             # Utility functions
├── requirements.txt       # Python dependencies
└── start_modern_demo.sh   # Quick start script
```

## 🛠️ Tech Stack

- **Frontend**: React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python
- **AI**: Google Gemini, Vertex AI, Google ADK
- **Database**: Firebase Firestore
- **Storage**: Google Cloud Storage
- **Deployment**: Google Cloud Run
- **Authentication**: Firebase Auth

## 📈 Current Status

✅ **Frontend**: Modern VenturusAI-inspired design fully functional  
✅ **Backend**: Enhanced FastAPI with full Google stack integration  
✅ **AI Agents**: Multi-agent system with Google ADK orchestration  
✅ **Multi-Modal**: Support for pitch decks, voice notes, and video  
✅ **Real-time**: Firebase integration for live collaboration  
✅ **File Upload**: Google Cloud Storage integration  

---

**Happy Analyzing!** 📈