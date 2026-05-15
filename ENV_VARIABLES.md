# Environment Variables Reference

This document lists all required environment variables for the VartaIQ AI application.

## Required Variables

### 1. DATABASE_URL
**Purpose:** PostgreSQL database connection string

**Format:**
```
postgresql://username:password@host:port/database?sslmode=require&channel_binding=require
```

**Current Setup:**
- Provider: Neon PostgreSQL
- Connection: Pooled connection for better performance
- SSL: Required for security

**Example:**
```env
DATABASE_URL=postgresql://neondb_owner:npg_dtfB5qLJT7YA@ep-misty-rice-anfocdnb-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

---

### 2. HF_API_TOKEN
**Purpose:** Hugging Face API authentication token for model inference

**Format:**
```
hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**How to Get:**
1. Create account at https://huggingface.co
2. Go to https://huggingface.co/settings/tokens
3. Click "New token"
4. Name: "VartaIQ API" (or any name)
5. Type: "Read" access is sufficient
6. Copy the generated token

**Example:**
```env
HF_API_TOKEN=hf_aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890
```

**Models Used:**
- `facebook/bart-large-cnn` - Summarization
- `cardiffnlp/twitter-roberta-base-sentiment-latest` - Sentiment Analysis
- `sentence-transformers/all-MiniLM-L6-v2` - Embeddings

**Rate Limits:**
- Free tier: ~1000 requests/day per model
- Pro tier: Higher limits available

---

## Setting Environment Variables

### Local Development (.env file)
Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://neondb_owner:npg_dtfB5qLJT7YA@ep-misty-rice-anfocdnb-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
HF_API_TOKEN=hf_your_actual_token_here
```

### Docker
Pass as environment variables:
```bash
docker run \
  -e DATABASE_URL="your_database_url" \
  -e HF_API_TOKEN="your_hf_token" \
  -p 8000:8000 \
  vartaiq-ai
```

Or use docker-compose:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - HF_API_TOKEN=${HF_API_TOKEN}
```

### Render
1. Go to your service dashboard
2. Navigate to "Environment" tab
3. Add variables:
   - Key: `DATABASE_URL`, Value: `your_database_url`
   - Key: `HF_API_TOKEN`, Value: `your_hf_token`

### Railway
1. Go to your project
2. Click "Variables" tab
3. Add variables:
   - `DATABASE_URL`
   - `HF_API_TOKEN`

### Heroku
```bash
heroku config:set DATABASE_URL="your_database_url"
heroku config:set HF_API_TOKEN="your_hf_token"
```

---

## Security Best Practices

✅ **DO:**
- Keep `.env` file in `.gitignore`
- Use environment variables in production
- Rotate tokens periodically
- Use read-only tokens when possible
- Enable SSL for database connections

❌ **DON'T:**
- Commit `.env` file to git
- Share tokens in public repositories
- Use the same token across multiple projects
- Hardcode credentials in source code
- Disable SSL for database connections

---

## Troubleshooting

### Missing DATABASE_URL
**Error:** `sqlalchemy.exc.ArgumentError: Could not parse SQLAlchemy URL`

**Solution:** Ensure `DATABASE_URL` is set in your `.env` file or environment

### Missing HF_API_TOKEN
**Error:** `[STARTUP ERROR] HF_API_TOKEN is not set.`

**Solution:** Add your Hugging Face token to the `.env` file

### Invalid HF_API_TOKEN
**Error:** `401 Unauthorized` from Hugging Face API

**Solution:** 
- Verify your token is correct
- Check if token has expired
- Generate a new token if needed

### Database Connection Failed
**Error:** `psycopg2.OperationalError: could not connect to server`

**Solution:**
- Verify database URL is correct
- Check if database server is running
- Ensure your IP is whitelisted
- Verify SSL settings

---

## Verification

To verify your environment variables are set correctly:

```python
import os
from dotenv import load_dotenv

load_dotenv()

print("DATABASE_URL:", "✓ Set" if os.getenv("DATABASE_URL") else "✗ Missing")
print("HF_API_TOKEN:", "✓ Set" if os.getenv("HF_API_TOKEN") else "✗ Missing")
```

Or simply run the application - it will fail fast with clear error messages if any required variables are missing.
