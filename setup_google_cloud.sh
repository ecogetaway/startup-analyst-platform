#!/bin/bash

# Google Cloud Setup Script for Startup Analyst Platform
echo "🚀 Setting up Google Cloud services for Startup Analyst Platform..."

# Set project ID
PROJECT_ID="startup-analyst-platform"
echo "📋 Project ID: $PROJECT_ID"

# Set default project
gcloud config set project $PROJECT_ID

echo "🔧 Enabling required Google Cloud APIs..."

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable logging.googleapis.com
gcloud services enable monitoring.googleapis.com
gcloud services enable storage.googleapis.com

echo "✅ APIs enabled successfully"

# Set up Vertex AI
echo "🤖 Setting up Vertex AI..."
gcloud ai models list --region=us-central1

# Set up Firestore
echo "🔥 Setting up Firestore..."
gcloud firestore databases create --region=us-central1

# Set up Cloud Storage bucket
echo "💾 Setting up Cloud Storage..."
gsutil mb gs://$PROJECT_ID-startup-analyst-data

# Set up service account
echo "🔐 Setting up service account..."
gcloud iam service-accounts create startup-analyst-sa \
    --display-name="Startup Analyst Service Account" \
    --description="Service account for Startup Analyst Platform"

# Grant necessary permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:startup-analyst-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:startup-analyst-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/datastore.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:startup-analyst-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.objectAdmin"

# Create and download service account key
echo "🔑 Creating service account key..."
gcloud iam service-accounts keys create service-account-key.json \
    --iam-account=startup-analyst-sa@$PROJECT_ID.iam.gserviceaccount.com

echo "✅ Google Cloud setup completed!"
echo ""
echo "📝 Next steps:"
echo "1. Set GOOGLE_APPLICATION_CREDENTIALS environment variable:"
echo "   export GOOGLE_APPLICATION_CREDENTIALS=\$(pwd)/service-account-key.json"
echo ""
echo "2. Test the setup:"
echo "   python3 test_gemini.py"
echo ""
echo "3. Deploy the application:"
echo "   gcloud run deploy startup-analyst --source ."
echo ""
echo "🎉 Your Google Cloud environment is ready for the hackathon!"
