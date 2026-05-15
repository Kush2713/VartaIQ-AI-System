# EC2 Deployment Guide - VartaIQ AI System

## EC2 Instance Details
- **Public IP:** 65.2.158.83
- **SSH Key:** Provided (RSA Private Key)

---

## Prerequisites

Before starting, ensure you have:
- ✅ EC2 instance running (Ubuntu/Amazon Linux)
- ✅ SSH private key saved
- ✅ Security group allows inbound traffic on port 8000 (or 80/443)
- ✅ Hugging Face API token
- ✅ Database URL (Neon PostgreSQL)

---

## Step 1: Save SSH Private Key

### On Windows:

1. Create a file named `vartaiq-key.pem` on your desktop
2. Copy the private key content into it
3. The key should look like:
   ```
   -----BEGIN RSA PRIVATE KEY-----
   [your key content]
   -----END RSA PRIVATE KEY-----
   ```

### Set Permissions (Windows):
```powershell
# Open PowerShell as Administrator
icacls "C:\Users\Admin\Desktop\vartaiq-key.pem" /inheritance:r
icacls "C:\Users\Admin\Desktop\vartaiq-key.pem" /grant:r "%USERNAME%:R"
```

---

## Step 2: Connect to EC2 Instance

### Using PowerShell (Windows):

```powershell
ssh -i "C:\Users\Admin\Desktop\vartaiq-key.pem" ubuntu@65.2.158.83
```

**Note:** If using Amazon Linux, replace `ubuntu` with `ec2-user`

### First Time Connection:
You'll see a message asking to confirm the host. Type `yes` and press Enter.

---

## Step 3: Update System Packages

Once connected to EC2:

```bash
# Update package list
sudo apt update

# Upgrade packages
sudo apt upgrade -y
```

---

## Step 4: Install Python 3.10

```bash
# Install Python 3.10 and pip
sudo apt install python3.10 python3.10-venv python3-pip -y

# Verify installation
python3.10 --version
```

---

## Step 5: Install Git

```bash
sudo apt install git -y

# Verify installation
git --version
```

---

## Step 6: Clone the Repository

```bash
# Navigate to home directory
cd ~

# Clone your repository
git clone https://github.com/Kush2713/VartaIQ-AI-System.git

# Navigate into the project
cd VartaIQ-AI-System
```

---

## Step 7: Create Virtual Environment

```bash
# Create virtual environment
python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your prompt
```

---

## Step 8: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

**Expected time:** 5-10 minutes

---

## Step 9: Configure Environment Variables

```bash
# Create .env file
nano .env
```

Add the following content:
```env
DATABASE_URL=postgresql://neondb_owner:npg_dtfB5qLJT7YA@ep-misty-rice-anfocdnb-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
HF_API_TOKEN=your_actual_huggingface_token_here
```

**Save and exit:**
- Press `Ctrl + X`
- Press `Y` to confirm
- Press `Enter` to save

---

## Step 10: Configure Security Group (AWS Console)

### Allow Inbound Traffic:

1. Go to AWS Console → EC2 → Security Groups
2. Find your instance's security group
3. Add inbound rules:

| Type | Protocol | Port Range | Source | Description |
|------|----------|------------|--------|-------------|
| Custom TCP | TCP | 8000 | 0.0.0.0/0 | VartaIQ API |
| SSH | TCP | 22 | Your IP | SSH Access |

**Optional (for production):**
- Port 80 (HTTP)
- Port 443 (HTTPS)

---

## Step 11: Test the Application

```bash
# Make sure you're in the project directory
cd ~/VartaIQ-AI-System

# Activate virtual environment (if not already active)
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

INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Test from your browser:
- Open: http://65.2.158.83:8000/docs

**Note:** Press `Ctrl + C` to stop the server

---

## Step 12: Run Application in Background (Production)

### Option A: Using nohup (Simple)

```bash
# Run in background
nohup python run.py > app.log 2>&1 &

# Check if running
ps aux | grep python

# View logs
tail -f app.log

# Stop the application
pkill -f "python run.py"
```

### Option B: Using systemd (Recommended for Production)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/vartaiq.service
```

Add the following content:
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

**Save and exit** (Ctrl + X, Y, Enter)

Enable and start the service:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable vartaiq

# Start the service
sudo systemctl start vartaiq

# Check status
sudo systemctl status vartaiq

# View logs
sudo journalctl -u vartaiq -f
```

**Service Management Commands:**
```bash
# Stop service
sudo systemctl stop vartaiq

# Restart service
sudo systemctl restart vartaiq

# Check status
sudo systemctl status vartaiq
```

---

## Step 13: Setup Nginx as Reverse Proxy (Optional but Recommended)

### Install Nginx:
```bash
sudo apt install nginx -y
```

### Configure Nginx:
```bash
sudo nano /etc/nginx/sites-available/vartaiq
```

Add the following configuration:
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

**Save and exit** (Ctrl + X, Y, Enter)

### Enable the configuration:
```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/vartaiq /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Enable Nginx to start on boot
sudo systemctl enable nginx
```

### Update Security Group:
Add inbound rule for port 80 (HTTP)

Now you can access the API at: http://65.2.158.83/docs

---

## Step 14: Setup SSL Certificate (Optional - HTTPS)

### Using Let's Encrypt (Free SSL):

**Note:** You need a domain name for this. If you don't have one, skip this step.

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate (replace with your domain)
sudo certbot --nginx -d yourdomain.com

# Auto-renewal is set up automatically
# Test renewal
sudo certbot renew --dry-run
```

---

## Troubleshooting

### Issue 1: Cannot connect via SSH
**Solution:**
- Check if EC2 instance is running
- Verify security group allows SSH (port 22) from your IP
- Ensure private key file has correct permissions

### Issue 2: Port 8000 not accessible
**Solution:**
- Check security group inbound rules
- Verify application is running: `ps aux | grep python`
- Check logs: `tail -f app.log` or `sudo journalctl -u vartaiq -f`

### Issue 3: Application crashes on startup
**Solution:**
```bash
# Check logs
sudo journalctl -u vartaiq -n 50

# Common issues:
# - Missing HF_API_TOKEN in .env
# - Database connection error
# - Missing dependencies
```

### Issue 4: Database connection error
**Solution:**
- Verify DATABASE_URL in .env is correct
- Check if EC2 can reach the database (firewall/security group)
- Test connection: `ping ep-misty-rice-anfocdnb-pooler.c-6.us-east-1.aws.neon.tech`

### Issue 5: HF API errors
**Solution:**
- Verify HF_API_TOKEN is correct in .env
- Check if you've hit rate limits
- Test token: https://huggingface.co/settings/tokens

---

## Monitoring and Maintenance

### Check Application Status:
```bash
sudo systemctl status vartaiq
```

### View Real-time Logs:
```bash
sudo journalctl -u vartaiq -f
```

### Restart Application:
```bash
sudo systemctl restart vartaiq
```

### Update Application:
```bash
cd ~/VartaIQ-AI-System
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart vartaiq
```

### Check Disk Space:
```bash
df -h
```

### Check Memory Usage:
```bash
free -h
```

### Check CPU Usage:
```bash
top
```

---

## Production Checklist

- [ ] EC2 instance running
- [ ] SSH access working
- [ ] Python 3.10 installed
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] .env file configured with correct values
- [ ] Security group allows port 8000 (or 80/443)
- [ ] Application runs successfully
- [ ] Systemd service configured
- [ ] Application starts on boot
- [ ] Nginx reverse proxy configured (optional)
- [ ] SSL certificate installed (optional)
- [ ] Monitoring set up

---

## Quick Commands Reference

```bash
# Connect to EC2
ssh -i "vartaiq-key.pem" ubuntu@65.2.158.83

# Navigate to project
cd ~/VartaIQ-AI-System

# Activate virtual environment
source venv/bin/activate

# Run application (foreground)
python run.py

# Check service status
sudo systemctl status vartaiq

# View logs
sudo journalctl -u vartaiq -f

# Restart service
sudo systemctl restart vartaiq

# Update code
git pull origin main
sudo systemctl restart vartaiq
```

---

## Access URLs

- **API Documentation:** http://65.2.158.83:8000/docs
- **Alternative Docs:** http://65.2.158.83:8000/redoc
- **Health Check:** http://65.2.158.83:8000/

**With Nginx (port 80):**
- **API Documentation:** http://65.2.158.83/docs

---

## Security Best Practices

1. ✅ Keep SSH key secure and never share it
2. ✅ Restrict SSH access to your IP only
3. ✅ Keep .env file secure (never commit to git)
4. ✅ Regularly update system packages
5. ✅ Use SSL certificate for production
6. ✅ Set up firewall rules properly
7. ✅ Monitor logs regularly
8. ✅ Set up automated backups

---

## Support

For issues, refer to:
- [SETUP.md](SETUP.md)
- [DEPLOYMENT.md](DEPLOYMENT.md)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Deployment completed! Your VartaIQ AI System is now running on EC2! 🚀**
