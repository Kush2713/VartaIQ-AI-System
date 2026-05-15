# EC2 Deployment - Amazon Linux Guide

## Your EC2 Instance
- **IP:** 65.2.158.83
- **User:** ec2-user (Amazon Linux)
- **Package Manager:** yum (not apt)

---

## Step 1: Update System Packages

```bash
# Update system
sudo yum update -y
```

---

## Step 2: Install Python 3.10

Amazon Linux 2023 comes with Python 3.9 by default. We need Python 3.10:

```bash
# Install Python 3.10
sudo yum install python3.10 -y

# Verify installation
python3.10 --version

# Install pip for Python 3.10
sudo yum install python3.10-pip -y

# Install development tools (needed for some Python packages)
sudo yum groupinstall "Development Tools" -y

# Install PostgreSQL development files (needed for psycopg2)
sudo yum install postgresql-devel -y
```

---

## Step 3: Install Git

```bash
# Install Git
sudo yum install git -y

# Verify installation
git --version
```

---

## Step 4: Clone Repository

```bash
# Navigate to home directory
cd ~

# Clone repository
git clone https://github.com/Kush2713/VartaIQ-AI-System.git

# Navigate into project
cd VartaIQ-AI-System
```

---

## Step 5: Create Virtual Environment

```bash
# Create virtual environment
python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your prompt
```

---

## Step 6: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install wheel (helps with some packages)
pip install wheel

# Install project dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

**Note:** This may take 5-10 minutes

---

## Step 7: Configure Environment Variables

```bash
# Create .env file
nano .env
```

Add this content:
```env
DATABASE_URL=postgresql://neondb_owner:npg_dtfB5qLJT7YA@ep-misty-rice-anfocdnb-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
HF_API_TOKEN=your_actual_huggingface_token_here
```

**Save and exit:**
- Press `Ctrl + X`
- Press `Y`
- Press `Enter`

---

## Step 8: Configure Security Group

1. Go to AWS Console → EC2 → Security Groups
2. Find your instance's security group
3. Add inbound rule:
   - Type: Custom TCP
   - Port: 8000
   - Source: 0.0.0.0/0
   - Description: VartaIQ API

---

## Step 9: Test the Application

```bash
# Make sure you're in the project directory
cd ~/VartaIQ-AI-System

# Activate virtual environment
source venv/bin/activate

# Run the application
python run.py
```

### Expected Output:
```
[Model] Summarizer API wrapper ready.
[Model] Sentiment API wrapper ready.
[Model] Embedding API wrapper ready.

All AI models ready (HF API - no local downloads).

INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Test in browser:
http://65.2.158.83:8000/docs

**Press Ctrl+C to stop**

---

## Step 10: Run in Background (Production)

### Option A: Using nohup

```bash
cd ~/VartaIQ-AI-System
source venv/bin/activate
nohup python run.py > app.log 2>&1 &

# Check if running
ps aux | grep python

# View logs
tail -f app.log

# Stop application
pkill -f "python run.py"
```

### Option B: Using systemd (Recommended)

Create service file:
```bash
sudo nano /etc/systemd/system/vartaiq.service
```

Add this content:
```ini
[Unit]
Description=VartaIQ AI System
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/VartaIQ-AI-System
Environment="PATH=/home/ec2-user/VartaIQ-AI-System/venv/bin"
ExecStart=/home/ec2-user/VartaIQ-AI-System/venv/bin/python run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Save and exit** (Ctrl+X, Y, Enter)

Enable and start:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable vartaiq

# Start service
sudo systemctl start vartaiq

# Check status
sudo systemctl status vartaiq

# View logs
sudo journalctl -u vartaiq -f
```

---

## Step 11: Setup Nginx (Optional)

```bash
# Install Nginx
sudo yum install nginx -y

# Start Nginx
sudo systemctl start nginx

# Enable on boot
sudo systemctl enable nginx

# Configure Nginx
sudo nano /etc/nginx/conf.d/vartaiq.conf
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name 65.2.158.83;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Save and exit** (Ctrl+X, Y, Enter)

Test and restart:
```bash
# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

Add port 80 to security group, then access at: http://65.2.158.83/docs

---

## Quick Commands Reference

```bash
# Connect to EC2
ssh -i "vartaiq-key.pem" ec2-user@65.2.158.83

# Navigate to project
cd ~/VartaIQ-AI-System

# Activate virtual environment
source venv/bin/activate

# Check service status
sudo systemctl status vartaiq

# Restart service
sudo systemctl restart vartaiq

# View logs
sudo journalctl -u vartaiq -f

# Update code
cd ~/VartaIQ-AI-System
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart vartaiq
```

---

## Troubleshooting

### Issue: Python 3.10 not available
```bash
# Check available Python versions
yum list available | grep python3

# If Python 3.10 not available, use Python 3.9
python3.9 -m venv venv
```

### Issue: psycopg2 installation fails
```bash
# Install PostgreSQL development files
sudo yum install postgresql-devel gcc python3-devel -y

# Then retry
pip install psycopg2-binary
```

### Issue: Permission denied
```bash
# Make sure you're using ec2-user (not ubuntu)
whoami

# Should output: ec2-user
```

### Issue: Port 8000 not accessible
- Check security group allows port 8000
- Check if application is running: `ps aux | grep python`
- Check logs: `tail -f ~/VartaIQ-AI-System/app.log`

---

## Complete Setup Script for Amazon Linux

Save this as `setup-amazon-linux.sh`:

```bash
#!/bin/bash

echo "=========================================="
echo "VartaIQ AI - Amazon Linux Setup"
echo "=========================================="

# Update system
echo "Updating system..."
sudo yum update -y

# Install Python 3.10
echo "Installing Python 3.10..."
sudo yum install python3.10 python3.10-pip -y

# Install development tools
echo "Installing development tools..."
sudo yum groupinstall "Development Tools" -y
sudo yum install postgresql-devel git -y

# Clone repository
echo "Cloning repository..."
cd ~
if [ -d "VartaIQ-AI-System" ]; then
    echo "Repository exists, pulling latest..."
    cd VartaIQ-AI-System
    git pull origin main
else
    git clone https://github.com/Kush2713/VartaIQ-AI-System.git
    cd VartaIQ-AI-System
fi

# Create virtual environment
echo "Creating virtual environment..."
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Create .env file
echo "Creating .env file..."
cat > .env << 'EOF'
DATABASE_URL=postgresql://neondb_owner:npg_dtfB5qLJT7YA@ep-misty-rice-anfocdnb-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
HF_API_TOKEN=REPLACE_WITH_YOUR_ACTUAL_HF_TOKEN
EOF

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "IMPORTANT: Edit .env and add your HF token:"
echo "  nano .env"
echo ""
echo "Then run:"
echo "  source venv/bin/activate"
echo "  python run.py"
echo ""
```

Run it:
```bash
chmod +x setup-amazon-linux.sh
./setup-amazon-linux.sh
```

---

## Access Your Application

- **API Docs:** http://65.2.158.83:8000/docs
- **ReDoc:** http://65.2.158.83:8000/redoc

---

**You're all set! Follow the steps above to deploy on Amazon Linux! 🚀**
