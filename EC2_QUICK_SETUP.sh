#!/bin/bash

# VartaIQ AI System - EC2 Quick Setup Script
# Run this script on your EC2 instance after connecting via SSH

echo "=========================================="
echo "VartaIQ AI System - EC2 Setup"
echo "=========================================="
echo ""

# Update system
echo "Step 1: Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python 3.10
echo ""
echo "Step 2: Installing Python 3.10..."
sudo apt install python3.10 python3.10-venv python3-pip git -y

# Verify Python installation
python3.10 --version

# Clone repository
echo ""
echo "Step 3: Cloning repository..."
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
echo "Step 4: Creating virtual environment..."
python3.10 -m venv venv

# Activate virtual environment
echo ""
echo "Step 5: Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Step 6: Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
echo ""
echo "Step 7: Downloading spaCy model..."
python -m spacy download en_core_web_sm

# Create .env file
echo ""
echo "Step 8: Creating .env file..."
cat > .env << 'EOF'
DATABASE_URL=postgresql://neondb_owner:npg_dtfB5qLJT7YA@ep-misty-rice-anfocdnb-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
HF_API_TOKEN=REPLACE_WITH_YOUR_ACTUAL_HF_TOKEN
EOF

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "IMPORTANT: Edit the .env file and add your Hugging Face API token:"
echo "  nano .env"
echo ""
echo "Then run the application:"
echo "  source venv/bin/activate"
echo "  python run.py"
echo ""
echo "Or set up as a systemd service (see EC2_DEPLOYMENT_GUIDE.md)"
echo ""
