# Deploy to EC2 - Quick Start Guide

## Your EC2 Details
- **IP Address:** 65.2.158.83
- **SSH Key:** vartaiq-key.pem (already created in this folder)
- **User:** ubuntu (or ec2-user for Amazon Linux)

---

## Option 1: Quick Deploy (Recommended)

### Step 1: Connect to EC2

**On Windows (PowerShell):**
```powershell
cd C:\Users\Admin\Desktop\VartaIQAI
ssh -i "vartaiq-key.pem" ubuntu@65.2.158.83
```

**Or simply double-click:** `connect-ec2.bat`

### Step 2: Run Quick Setup Script

Once connected to EC2, run these commands:

```bash
# Download the setup script
curl -o setup.sh https://raw.githubusercontent.com/Kush2713/VartaIQ-AI-System/main/EC2_QUICK_SETUP.sh

# Make it executable
chmod +x setup.sh

# Run the setup
./setup.sh
```

### Step 3: Add Your Hugging Face Token

```bash
# Edit the .env file
nano .env

# Replace REPLACE_WITH_YOUR_ACTUAL_HF_TOKEN with your actual token
# Press Ctrl+X, then Y, then Enter to save
```

### Step 4: Run the Application

```bash
# Make sure you're in the project directory
cd ~/VartaIQ-AI-System

# Activate virtual environment
source venv/bin/activate

# Run the application
python run.py
```

### Step 5: Test It

Open in your browser: http://65.2.158.83:8000/docs

---

## Option 2: Manual Step-by-Step

If the quick setup doesn't work, follow the detailed guide in `EC2_DEPLOYMENT_GUIDE.md`

---

## Configure Security Group (AWS Console)

**IMPORTANT:** Before accessing the application, configure your EC2 security group:

1. Go to AWS Console → EC2 → Instances
2. Select your instance
3. Click on "Security" tab
4. Click on the security group link
5. Click "Edit inbound rules"
6. Add these rules:

| Type | Port | Source | Description |
|------|------|--------|-------------|
| SSH | 22 | My IP | SSH Access |
| Custom TCP | 8000 | 0.0.0.0/0 | VartaIQ API |

7. Click "Save rules"

---

## Run in Background (Production)

### Quick Method (nohup):
```bash
cd ~/VartaIQ-AI-System
source venv/bin/activate
nohup python run.py > app.log 2>&1 &
```

### Check if running:
```bash
ps aux | grep python
```

### View logs:
```bash
tail -f ~/VartaIQ-AI-System/app.log
```

### Stop the application:
```bash
pkill -f "python run.py"
```

---

## Setup as System Service (Recommended)

### Create service file:
```bash
sudo nano /etc/systemd/system/vartaiq.service
```

### Add this content:
```ini
[Unit]
Description=VartaIQ AI System
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/VartaIQ-AI-System
Environment="PATH=/home/ubuntu/VartaIQ-AI-System/venv/bin"
ExecStart=/home/ubuntu/VartaIQ-AI-System/venv/bin/python run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable vartaiq
sudo systemctl start vartaiq
sudo systemctl status vartaiq
```

---

## Troubleshooting

### Can't connect via SSH?
```powershell
# Check key permissions (Windows PowerShell as Admin)
icacls "C:\Users\Admin\Desktop\VartaIQAI\vartaiq-key.pem" /inheritance:r
icacls "C:\Users\Admin\Desktop\VartaIQAI\vartaiq-key.pem" /grant:r "%USERNAME%:R"
```

### Application won't start?
```bash
# Check logs
tail -f ~/VartaIQ-AI-System/app.log

# Or if using systemd
sudo journalctl -u vartaiq -f
```

### Port 8000 not accessible?
- Check AWS Security Group allows port 8000
- Check if application is running: `ps aux | grep python`
- Check EC2 instance is running in AWS Console

---

## Quick Commands

```bash
# Connect to EC2
ssh -i "vartaiq-key.pem" ubuntu@65.2.158.83

# Check service status
sudo systemctl status vartaiq

# Restart service
sudo systemctl restart vartaiq

# View logs
sudo journalctl -u vartaiq -f

# Update code
cd ~/VartaIQ-AI-System
git pull origin main
sudo systemctl restart vartaiq
```

---

## Access Your Application

- **API Docs:** http://65.2.158.83:8000/docs
- **ReDoc:** http://65.2.158.83:8000/redoc

---

## Next Steps

1. ✅ Deploy to EC2 (follow steps above)
2. ⏳ Set up Nginx reverse proxy (optional - see EC2_DEPLOYMENT_GUIDE.md)
3. ⏳ Configure domain name (optional)
4. ⏳ Set up SSL certificate (optional)
5. ⏳ Set up monitoring and alerts

---

## Need Help?

See detailed documentation:
- **Full Guide:** EC2_DEPLOYMENT_GUIDE.md
- **Setup Guide:** SETUP.md
- **Deployment Guide:** DEPLOYMENT.md

---

**Ready to deploy? Start with Step 1 above! 🚀**
