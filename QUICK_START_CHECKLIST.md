# Quick Start Checklist ✅

Follow this checklist to get your VartaIQ AI application up and running.

## ⚠️ IMPORTANT - Action Required

Before running the application, you **MUST** complete step 1 below!

---

## 1. 🔑 Get Hugging Face API Token (REQUIRED)

**Status:** ⚠️ **ACTION REQUIRED**

The application will NOT start without this token!

### Steps:
1. Go to https://huggingface.co
2. Create a free account (if you don't have one)
3. Go to https://huggingface.co/settings/tokens
4. Click "New token"
5. Name it: `VartaIQ API`
6. Select: **Read** access
7. Click "Generate token"
8. **Copy the token** (starts with `hf_`)

### Update .env file:
Open `.env` file and replace:
```env
HF_API_TOKEN=REPLACE_WITH_YOUR_ACTUAL_HF_TOKEN
```

With your actual token:
```env
HF_API_TOKEN=hf_your_actual_token_here
```

**Example token format:** `hf_aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890`

---

## 2. ✅ Database Configuration (Already Done)

**Status:** ✅ **COMPLETED**

The database URL is already configured in `.env`:
```env
DATABASE_URL=postgresql://neondb_owner:npg_dtfB5qLJT7YA@ep-misty-rice-anfocdnb-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

No action needed unless you want to use a different database.

---

## 3. 🐍 Python Environment Setup

**Status:** ⏳ **TODO**

### Check Python Version:
```bash
python --version
```

**Required:** Python 3.10, 3.11, or 3.12 (NOT 3.13+)

### Create Virtual Environment:
```bash
# Windows
py -3.10 -m venv venv
venv\Scripts\activate

# Linux/Mac
python3.10 -m venv venv
source venv/bin/activate
```

---

## 4. 📦 Install Dependencies

**Status:** ⏳ **TODO**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected time:** 2-5 minutes

---

## 5. 📥 Download spaCy Model

**Status:** ⏳ **TODO**

```bash
python -m spacy download en_core_web_sm
```

**Size:** ~40MB
**Expected time:** 30 seconds - 1 minute

---

## 6. 🚀 Run the Application

**Status:** ⏳ **TODO**

```bash
python run.py
```

### Expected Output:
```
[Model] Summarizer API wrapper ready.
[Model] Sentiment API wrapper ready.
[Model] Embedding API wrapper ready.

All AI models ready (HF API - no local downloads).

INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 7. 🧪 Test the API

**Status:** ⏳ **TODO**

### Open in browser:
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

### Test the `/analyze` endpoint:
1. Go to http://127.0.0.1:8000/docs
2. Click on `POST /analyze`
3. Click "Try it out"
4. Use the sample request body
5. Click "Execute"
6. Check the response

---

## 📋 Verification Checklist

Before running the application, verify:

- [ ] Python 3.10, 3.11, or 3.12 is installed
- [ ] Virtual environment is created and activated
- [ ] All dependencies are installed (`pip install -r requirements.txt`)
- [ ] spaCy model is downloaded (`python -m spacy download en_core_web_sm`)
- [ ] `.env` file exists in project root
- [ ] `DATABASE_URL` is set in `.env` (already done ✅)
- [ ] **`HF_API_TOKEN` is set in `.env` with your actual token** ⚠️
- [ ] `.env` file is NOT committed to git (it's in `.gitignore` ✅)

---

## 🚨 Common Issues

### Issue 1: Application won't start
**Error:** `[STARTUP ERROR] HF_API_TOKEN is not set.`

**Solution:** 
- Open `.env` file
- Replace `REPLACE_WITH_YOUR_ACTUAL_HF_TOKEN` with your actual HF token
- Make sure there are no extra spaces or quotes

### Issue 2: Python version error
**Error:** `Python 3.13 is not supported.`

**Solution:** 
- Install Python 3.10, 3.11, or 3.12
- Use: `py -3.10 -m venv venv` (Windows) or `python3.10 -m venv venv` (Linux/Mac)

### Issue 3: spaCy model not found
**Error:** `Can't find model 'en_core_web_sm'`

**Solution:** 
```bash
python -m spacy download en_core_web_sm
```

### Issue 4: Database connection error
**Error:** `could not connect to server`

**Solution:** 
- Check your internet connection
- Verify the `DATABASE_URL` in `.env` is correct
- The Neon database should be accessible from anywhere

### Issue 5: HF API 401 Unauthorized
**Error:** `401 Unauthorized` from Hugging Face API

**Solution:** 
- Verify your HF token is correct
- Make sure the token starts with `hf_`
- Generate a new token if needed

---

## 📚 Need More Help?

- **Setup Guide:** [SETUP.md](SETUP.md)
- **Deployment Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Environment Variables:** [ENV_VARIABLES.md](ENV_VARIABLES.md)
- **Changes Summary:** [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)
- **API Documentation:** [VartaIQ_AI_Module_Documentation.md](VartaIQ_AI_Module_Documentation.md)

---

## 🎉 Success!

If you see this output, you're ready to go:
```
All AI models ready (HF API - no local downloads).
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Next Steps:**
1. Open http://127.0.0.1:8000/docs
2. Test the API
3. Start analyzing meetings!

---

## 🚀 Deployment

Ready to deploy to production?

See [DEPLOYMENT.md](DEPLOYMENT.md) for instructions on deploying to:
- Render
- Railway
- Heroku
- Docker
- Any platform that supports Python

**Remember:** Set both `DATABASE_URL` and `HF_API_TOKEN` as environment variables on your deployment platform!

---

**Last Updated:** After database and HF API configuration changes
