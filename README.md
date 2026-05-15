# VartaIQ AI - Meeting Analysis System

An intelligent AI-powered meeting analysis system that automatically processes meeting transcripts and generates comprehensive insights including summaries, action items, decisions, sentiment analysis, and more.

## Quick Start

### Prerequisites
- Python 3.10, 3.11, or 3.12
- Neon PostgreSQL database (or any PostgreSQL)
- Hugging Face account (free)

### Setup in 3 Steps

1. **Clone and install dependencies:**
   ```bash
   cd VartaIQAI
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

2. **Configure environment variables:**
   
   Create a `.env` file:
   ```env
   DATABASE_URL=your_postgresql_url
   HF_API_TOKEN=your_huggingface_token
   ```
   
   Get your HF token: https://huggingface.co/settings/tokens

3. **Run the application:**
   ```bash
   python run.py
   ```
   
   API will be available at: http://127.0.0.1:8000

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Detailed setup instructions
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
- **[ENV_VARIABLES.md](ENV_VARIABLES.md)** - Environment variables reference
- **[CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)** - Recent configuration changes
- **[VartaIQ_AI_Module_Documentation.md](VartaIQ_AI_Module_Documentation.md)** - Complete API documentation

## Features

### AI-Powered Analysis
- **Smart Summarization** - Automatic meeting summaries
- **Action Items Detection** - Identifies tasks and assignments
- **Decision Tracking** - Captures key decisions made
- **Sentiment Analysis** - Analyzes emotional tone and risks
- **Speaker Analysis** - Evaluates participation and engagement
- **Topic Detection** - Identifies main discussion topics
- **Useless Talk Detection** - Filters out off-topic content
- **Meeting Scoring** - Overall productivity assessment

### Technical Features
- **Cloud-Based AI** - Uses Hugging Face Inference API (no local model downloads)
- **PostgreSQL Database** - Stores all analysis results
- **Secure** - SSL-enabled database connections
- **Docker Ready** - Containerized deployment
- **REST API** - FastAPI with automatic documentation
- **Fast** - Optimized processing pipeline

## Architecture

### AI Models (via Hugging Face API)
- **Summarization:** facebook/bart-large-cnn
- **Sentiment Analysis:** cardiffnlp/twitter-roberta-base-sentiment-latest
- **Embeddings:** sentence-transformers/all-MiniLM-L6-v2
- **NLP Processing:** spaCy en_core_web_sm (local)

### Tech Stack
- **Backend:** FastAPI + Python 3.10+
- **Database:** PostgreSQL (Neon hosted)
- **AI/ML:** Hugging Face Transformers, spaCy, scikit-learn
- **Deployment:** Docker, Render, Railway, Heroku compatible

## Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `HF_API_TOKEN` | Hugging Face API token | `hf_xxxxxxxxxxxxx` |

See [ENV_VARIABLES.md](ENV_VARIABLES.md) for detailed configuration.

## API Endpoints

### Main Endpoint
```
POST /analyze
```

**Input:** Meeting transcript (JSON)
```json
{
  "transcript": [
    {"speaker": "John", "text": "Let's discuss the deployment..."},
    {"speaker": "Sarah", "text": "I'll handle the database migration..."}
  ]
}
```

**Output:** Complete analysis including:
- Summary
- Action items
- Decisions
- Topics
- Sentiment analysis
- Speaker analysis
- Meeting score
- And more...

### Documentation
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Docker Deployment

```bash
# Build
docker build -t vartaiq-ai .

# Run
docker run \
  -e DATABASE_URL="your_db_url" \
  -e HF_API_TOKEN="your_token" \
  -p 8000:8000 \
  vartaiq-ai
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for platform-specific instructions.

## Benefits

### Space Efficient
- **No large model downloads** (~500MB+ saved)
- **Minimal local storage** (only ~40MB for spaCy)
- **Fast deployment** (no model download time)

### Cost Effective
- **Free tier available** (Hugging Face API)
- **No GPU required** (models run on HF servers)
- **Scalable** (automatic load balancing)

### Developer Friendly
- **Easy setup** (just 2 environment variables)
- **Auto documentation** (FastAPI Swagger)
- **Type safety** (Pydantic schemas)

## Example Use Cases

1. **Team Meetings** - Analyze daily standups, sprint planning, retrospectives
2. **Client Calls** - Track decisions, action items, and commitments
3. **Board Meetings** - Generate executive summaries and key decisions
4. **Training Sessions** - Identify key topics and participant engagement
5. **Sales Calls** - Analyze sentiment and track follow-up actions

## 🛠️ Development

### Project Structure
```
VartaIQAI/
├── app/
│   ├── config/          # AI configuration
│   ├── db/              # Database models
│   ├── modules/         # AI processing modules
│   ├── services/        # Business logic
│   ├── main.py          # FastAPI app
│   ├── routes.py        # API endpoints
│   └── schemas.py       # Pydantic models
├── .env                 # Environment variables (not in git)
├── .env.example         # Template for .env
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
└── run.py              # Application entry point
```

### Running Tests
```bash
# Install dev dependencies
pip install pytest pytest-cov

# Run tests
pytest

# With coverage
pytest --cov=app
```

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Support

For issues and questions:
- Check the documentation files
- Review [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md) for recent updates
- See [VartaIQ_AI_Module_Documentation.md](VartaIQ_AI_Module_Documentation.md) for API details

## Roadmap

- [ ] Real-time transcription integration
- [ ] Multi-language support
- [ ] Custom model fine-tuning
- [ ] Advanced analytics dashboard
- [ ] Export to various formats (PDF, DOCX, etc.)
- [ ] Integration with calendar apps
- [ ] Slack/Teams bot integration

---

**Built with ❤️ using FastAPI, Hugging Face, and spaCy**
