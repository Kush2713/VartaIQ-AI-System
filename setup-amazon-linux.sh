#!/bin/bash

# VartaIQ AI System - Amazon Linux Setup Script
# Run this on your EC2 instance (Amazon Linux)

echo "=========================================="
echo "VartaIQ AI - Amazon Linux Setup"
echo "=========================================="
echo ""

# Update system
echo "Step 1: Updating system packages..."
sudo yum update -y

# Install Python 3.10
echo ""
echo "Step 2: Installing Python 3.10..."
sudo yum install python3.10 python3.10-pip -y

# Verify Python
python3.10 --version

# Install development tools
echo ""
echo "Step 3: Installing development tools..."
sudo yum groupinstall "Development Tools" -y
sudo yum install postgresql-devel git -y

# Clone repository
echo ""
echo "Step 4: Cloning repository..."
cd ~
if [ -d "VartaIQ-AI-System" ]; then
    echo "Repository already exists. Pulling latest changes..."
    cd VartaIQ-AI-System
    git pull origin main
else
    git clone https://github.com/Kush2713/VartaIQ-AI-System.git
    cd VartaIQ-AI-System
fi

# Create virtual environment
echo ""
echo "Step 5: Creating virtual environment..."
python3.10 -m venv venv

# Activate virtual environment
echo ""
echo "Step 6: Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Step 7: Installing dependencies (this may take 5-10 minutes)..."
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt

# Download spaCy model
echo ""
echo "Step 8: Downloading spaCy model..."
python -m spacy download en_core_web_sm

# Create .env file
echo ""
echo "Step 9: Creating .env file..."
cat > .env << 'EOF'
DATABASE_URL=postgresql://neondb_owner:npg_dtfB5qLJT7YA@ep-misty-rice-anfocdnb-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
HF_API_TOKEN=REPLACE_WITH_YOUR_ACTUAL_HF_TOKEN
EOF

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "⚠️  IMPORTANT: Edit the .env file and add your Hugging Face API token:"
echo ""
echo "  nano .env"
echo ""
echo "Replace REPLACE_WITH_YOUR_ACTUAL_HF_TOKEN with your actual token from:"
echo "  https://huggingface.co/settings/tokens"
echo ""
echo "Then run the application:"
echo ""
echo "  cd ~/VartaIQ-AI-System"
echo "  source venv/bin/activate"
echo "  python run.py"
echo ""
echo "Or set up as a systemd service (see EC2_AMAZON_LINUX_SETUP.md)"
echo ""
echo "Access the API at: http://65.2.158.83:8000/docs"
echo ""
echo "Don't forget to configure AWS Security Group to allow port 8000!"
echo ""
