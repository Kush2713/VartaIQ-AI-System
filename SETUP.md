# Setup Guide

## Prerequisites

- Python 3.10, 3.11, or 3.12 (Python 3.13+ not supported)
- Neon PostgreSQL database (or any PostgreSQL database)
- Hugging Face account and API token

## Step 1: Clone and Navigate

```bash
cd VartaIQAI
```

## Step 2: Create Virtual Environment

```bash
# Windows
py -3.10 -m venv venv
venv\Scripts\activate

# Linux/Mac
python3.10 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 4: Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

## Step 5: Configure Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=postgresql://neondb_owner:npg_dtfB5qLJT7YA@ep-misty-rice-anfocdnb-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

# Hugging Face API Configuration
HF_API_TOKEN=hf_your_actual_token_here
```

**Get your Hugging Face token:**
1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Give it a name (e.g., "VartaIQ API")
4. Select "Read" access
5. Copy the token and paste it in your `.env` file

## Step 6: Run the Application

```bash
python run.py
```

The application will start on http://127.0.0.1:8000

## Step 7: Test the API

Open your browser and go to:
- API Documentation: http://127.0.0.1:8000/docs
- Alternative Docs: http://127.0.0.1:8000/redoc

## Troubleshooting

### Python Version Error
```
[ERROR] Python 3.13 is not supported.
```
**Solution:** Use Python 3.10, 3.11, or 3.12

### Missing HF_API_TOKEN
```
[STARTUP ERROR] HF_API_TOKEN is not set.
```
**Solution:** Add your Hugging Face token to the `.env` file

### Database Connection Error
**Solution:** 
- Verify your `DATABASE_URL` is correct
- Check if the database exists
- Ensure your IP is whitelisted (Neon allows all by default)

### spaCy Model Not Found
```
Can't find model 'en_core_web_sm'
```
**Solution:** Run `python -m spacy download en_core_web_sm`

### HF API Rate Limiting
If you're using the free tier, you might hit rate limits with heavy usage.
**Solution:** Consider upgrading to HF Pro or implementing request caching

## Docker Deployment

Build the Docker image:
```bash
docker build -t vartaiq-ai .
```

Run the container:
```bash
docker run -e DATABASE_URL="your_db_url" -e HF_API_TOKEN="your_token" -p 8000:8000 vartaiq-ai
```

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for various platforms.

## What's Using the HF API?

The following models run entirely on Hugging Face servers (no local downloads):
- ✅ Summarization model (facebook/bart-large-cnn)
- ✅ Sentiment analysis (cardiffnlp/twitter-roberta-base-sentiment-latest)
- ✅ Embeddings (sentence-transformers/all-MiniLM-L6-v2)

The following still runs locally:
- 📦 spaCy (en_core_web_sm) - ~40MB - Used for linguistic analysis

**Total space saved:** ~500MB+ by using HF API instead of local models!
