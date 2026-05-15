# Deployment Guide

## Environment Variables

This project requires the following environment variables:

### 1. Database Configuration

The application reads the database URL from the `DATABASE_URL` environment variable.

**Local Development:**
- The `.env` file contains the database URL
- The application automatically loads it via `python-dotenv`

**Production Deployment:**
- Set the `DATABASE_URL` environment variable in your deployment platform
- The format should be: `postgresql://username:password@host:port/database?sslmode=require`

### 2. Hugging Face API Token

The application uses Hugging Face Inference API for all AI models (summarization, sentiment analysis, embeddings).

**Required:** `HF_API_TOKEN`

**How to get your token:**
1. Go to https://huggingface.co/settings/tokens
2. Create a new token (read access is sufficient)
3. Add it to your `.env` file or deployment platform environment variables

**Benefits of using HF API:**
- ✅ No model downloads required (saves ~500MB+ disk space)
- ✅ No GPU needed locally
- ✅ Faster deployment times
- ✅ Always uses latest model versions
- ✅ Automatic scaling and load balancing

## Current Database

- **Provider:** Neon PostgreSQL
- **Connection:** Configured in `.env` file (not committed to git)
- **Fallback:** The `app/db/database.py` has a hardcoded fallback to the Neon database

### Deployment Platforms

#### Render / Railway / Heroku
1. Add `DATABASE_URL` as an environment variable in the dashboard
2. Add `HF_API_TOKEN` as an environment variable in the dashboard
3. The application will automatically use them

#### Docker
1. Pass the environment variables when running the container:
   ```bash
   docker run \
     -e DATABASE_URL="your_database_url" \
     -e HF_API_TOKEN="your_hf_token" \
     -p 8000:8000 \
     your-image
   ```

2. Or use docker-compose with an `.env` file:
   ```yaml
   version: '3.8'
   services:
     app:
       build: .
       ports:
         - "8000:8000"
       env_file:
         - .env
   ```

### Database Initialization

The application automatically creates tables on startup via:
```python
Base.metadata.create_all(bind=engine)
```

This runs in `app/main.py` when the FastAPI application starts.

### Security Notes

- ✅ `.env` file is in `.gitignore` (credentials not committed)
- ✅ SSL mode is enabled (`sslmode=require`)
- ✅ Channel binding is required for additional security
- ✅ HF API token is kept secure in environment variables
- ⚠️ For production, always use environment variables instead of hardcoded values

### AI Models

**All models run via Hugging Face Inference API:**
- `facebook/bart-large-cnn` - Text summarization
- `cardiffnlp/twitter-roberta-base-sentiment-latest` - Sentiment analysis
- `sentence-transformers/all-MiniLM-L6-v2` - Semantic embeddings
- `spacy/en_core_web_sm` - NLP processing (downloaded during Docker build)

**Note:** spaCy model is still downloaded during Docker build as it's used for linguistic analysis (POS tagging, sentence segmentation, etc.) which doesn't have a direct API equivalent.

### Testing the Connection

Run the application locally:
```bash
python run.py
```

The application will:
1. Load the `.env` file
2. Connect to the Neon database
3. Create tables if they don't exist
4. Start the FastAPI server on http://127.0.0.1:8000

### Troubleshooting

**Connection Issues:**
- Verify the database URL is correct
- Check if your IP is whitelisted (Neon allows all by default)
- Ensure SSL certificates are up to date

**Table Creation Issues:**
- Check database permissions
- Verify the database exists
- Review logs for SQLAlchemy errors
