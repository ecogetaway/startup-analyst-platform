# 🚂 Railway Deployment Guide

## Overview
This guide covers deploying the Startup Analyst Platform to Railway, a modern cloud platform for full-stack applications.

## Prerequisites
- Railway account (free tier available)
- GitHub repository connected
- Node.js and Python dependencies

## Deployment Steps

### 1. Connect to Railway
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `ecogetaway/startup-analyst-platform`

### 2. Configure Build Settings
Railway will auto-detect the configuration from:
- `railway.json` - Railway-specific settings
- `nixpacks.toml` - Build configuration
- `Procfile` - Start command

### 3. Environment Variables (Optional)
Add these if needed:
```
NODE_ENV=production
REACT_APP_DEMO_MODE=true
```

### 4. Deploy
- Railway will automatically build and deploy
- Build process: ~3-5 minutes
- Frontend will be available at the provided Railway URL

## Configuration Files

### railway.json
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd frontend && npm start",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### nixpacks.toml
```toml
[phases.setup]
nixPkgs = ["nodejs", "npm", "python3", "pip"]

[phases.install]
cmds = [
  "cd frontend && npm install",
  "pip install -r requirements.txt"
]

[phases.build]
cmds = [
  "cd frontend && npm run build"
]

[start]
cmd = "cd frontend && npm start"
```

### Procfile
```
web: cd frontend && npm start
```

## Build Process
1. **Setup**: Install Node.js, npm, Python3, pip
2. **Install**: Install frontend dependencies and Python requirements
3. **Build**: Build React frontend for production
4. **Start**: Serve the application

## Features
- ✅ **Auto-deployment** from GitHub pushes
- ✅ **Free tier** available
- ✅ **Custom domains** supported
- ✅ **Environment variables** management
- ✅ **Logs and monitoring** built-in
- ✅ **HTTPS** by default

## Demo Features
- 🎭 **Demo API** with 2-second analysis
- 📊 **Mock results** for hackathon demo
- 🚀 **Fast loading** and responsive UI
- 📱 **Mobile-friendly** design

## Troubleshooting

### Build Fails
- Check Railway logs for specific errors
- Ensure all dependencies are in `package.json` and `requirements.txt`
- Verify file paths in configuration

### App Won't Start
- Check the start command in `Procfile`
- Verify port configuration (Railway uses PORT env var)
- Review application logs

### Performance Issues
- Railway free tier has resource limits
- Consider upgrading for production use
- Monitor usage in Railway dashboard

## Next Steps
1. Deploy to Railway
2. Test the live demo
3. Share Railway URL with judges
4. Create demo video using Railway link

## Support
- Railway Documentation: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- GitHub Issues: For code-related problems
