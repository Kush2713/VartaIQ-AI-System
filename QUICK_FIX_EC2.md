# Quick Fix for EC2 - Copy & Paste These Commands

## You're connected to EC2 as: ec2-user@ip-172-31-32-87

---

## Copy and paste these commands one by one:

### 1. Install Python 3.9 and tools
```bash
sudo yum install python3.9 python3.9-pip python3.9-devel -y
```

### 2. Install development tools
```bash
sudo yum groupinstall "Development Tools" -y
```

### 3. Install PostgreSQL development files
```bash
sudo yum install postgresql-devel git -y
```

### 4. Clone the repository
```bash
cd ~
git clone https://github.com/Kush2713/VartaIQ-AI-System.git
cd VartaIQ-AI-System
```

### 5. Create virtual environment
```bash
python3.9 -m venv venv
```

### 6. Activate virtual environment
```bash
source venv/bin/activate
```

### 7. Install Python dependencies
```bash
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt
```

### 8. Download spaCy model
```bash
python -m spacy download en_core_web_sm
```

### 9. Create .env file
```bash
nano .env
```

**Paste this content:**
```env
DATABASE_URL=postgresql://neondb_owner:npg_dtfB5qLJT7YA@ep-misty-rice-anfocdnb-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
HF_API_TOKEN=your_actual_huggingface_token_here
```

**Save:** Press `Ctrl+X`, then `Y`, then `Enter`

### 10. Run the application
```bash
python run.py
```

---

## Expected Output:
```
[Model] Summarizer API wrapper ready.
[Model] Sentiment API wrapper ready.
[Model] Embedding API wrapper ready.

All AI models ready (HF API - no local downloads).

INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## Access Your API:
http://65.2.158.83:8000/docs

**Note:** Make sure AWS Security Group allows port 8000!

---

## To Stop the Application:
Press `Ctrl+C`

---

## To Run in Background:
```bash
nohup python run.py > app.log 2>&1 &
```

## To Check if Running:
```bash
ps aux | grep python
```

## To View Logs:
```bash
tail -f app.log
```

## To Stop Background Process:
```bash
pkill -f "python run.py"
```

---

## If You Get Disconnected:

### Reconnect:
```bash
ssh -i "vartaiq-key.pem" ec2-user@65.2.158.83
```

### Navigate to project:
```bash
cd ~/VartaIQ-AI-System
```

### Activate virtual environment:
```bash
source venv/bin/activate
```

### Run application:
```bash
python run.py
```

---

## Configure AWS Security Group:

1. Go to AWS Console → EC2 → Security Groups
2. Find your instance's security group
3. Add inbound rule:
   - Type: Custom TCP
   - Port: 8000
   - Source: 0.0.0.0/0
   - Description: VartaIQ API

---

**That's it! Your application should be running! 🚀**
