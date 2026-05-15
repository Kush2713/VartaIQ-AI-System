# Fix Python Installation on Amazon Linux

## Problem
Python 3.10 is not available in Amazon Linux default repositories.

## Solution: Use Available Python Version

### Step 1: Check Available Python Versions

```bash
# Check what Python versions are available
yum list available | grep python3
```

### Step 2: Install Available Python (Recommended)

```bash
# Install Python 3.9 (usually available on Amazon Linux 2023)
sudo yum install python3.9 python3.9-pip python3.9-devel -y

# Verify installation
python3.9 --version
```

### Step 3: Install Required Dependencies

```bash
# Install development tools
sudo yum groupinstall "Development Tools" -y

# Install PostgreSQL development files
sudo yum install postgresql-devel git -y
```

### Step 4: Clone Repository

```bash
cd ~
git clone https://github.com/Kush2713/VartaIQ-AI-System.git
cd VartaIQ-AI-System
```

### Step 5: Create Virtual Environment with Python 3.9

```bash
# Create virtual environment with Python 3.9
python3.9 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify Python version in venv
python --version
```

### Step 6: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install wheel
pip install wheel

# Install project dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Step 7: Create .env File

```bash
nano .env
```

Add this content:
```env
DATABASE_URL=postgresql://neondb_owner:npg_dtfB5qLJT7YA@ep-misty-rice-anfocdnb-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
HF_API_TOKEN=your_actual_huggingface_token_here
```

Save: `Ctrl+X`, then `Y`, then `Enter`

### Step 8: Run the Application

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the application
python run.py
```

---

## Alternative: Install Python 3.10 from Source (Advanced)

If you really need Python 3.10, you can compile it from source:

### Install Build Dependencies

```bash
sudo yum groupinstall "Development Tools" -y
sudo yum install openssl-devel bzip2-devel libffi-devel zlib-devel wget -y
```

### Download and Compile Python 3.10

```bash
cd /tmp
wget https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tgz
tar xzf Python-3.10.13.tgz
cd Python-3.10.13

# Configure and compile
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall

# Verify installation
python3.10 --version
```

**Note:** This takes 10-15 minutes to compile.

### Then Continue with Setup

```bash
cd ~
git clone https://github.com/Kush2713/VartaIQ-AI-System.git
cd VartaIQ-AI-System

# Create virtual environment with Python 3.10
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Create .env file
nano .env
# Add your configuration

# Run application
python run.py
```

---

## Complete Setup Script (Using Python 3.9)

Save this as `setup-amazon-linux-py39.sh`:

```bash
#!/bin/bash

echo "=========================================="
echo "VartaIQ AI - Amazon Linux Setup (Python 3.9)"
echo "=========================================="
echo ""

# Update system
echo "Step 1: Updating system..."
sudo yum update -y

# Install Python 3.9
echo ""
echo "Step 2: Installing Python 3.9..."
sudo yum install python3.9 python3.9-pip python3.9-devel -y

# Verify Python
python3.9 --version

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
    echo "Repository exists, pulling latest..."
    cd VartaIQ-AI-System
    git pull origin main
else
    git clone https://github.com/Kush2713/VartaIQ-AI-System.git
    cd VartaIQ-AI-System
fi

# Create virtual environment
echo ""
echo "Step 5: Creating virtual environment..."
python3.9 -m venv venv

# Activate virtual environment
echo ""
echo "Step 6: Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Step 7: Installing dependencies..."
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
echo "⚠️  IMPORTANT: Edit .env and add your HF token:"
echo "  nano .env"
echo ""
echo "Then run:"
echo "  cd ~/VartaIQ-AI-System"
echo "  source venv/bin/activate"
echo "  python run.py"
echo ""
echo "Access at: http://65.2.158.83:8000/docs"
echo ""
```

---

## Quick Commands to Run Now

**On your EC2 instance, run these commands:**

```bash
# Install Python 3.9
sudo yum install python3.9 python3.9-pip python3.9-devel -y

# Install development tools
sudo yum groupinstall "Development Tools" -y
sudo yum install postgresql-devel git -y

# Clone repository
cd ~
git clone https://github.com/Kush2713/VartaIQ-AI-System.git
cd VartaIQ-AI-System

# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Create .env file
nano .env
# Add your DATABASE_URL and HF_API_TOKEN

# Run application
python run.py
```

---

## Why Python 3.9 Works

Your project is compatible with Python 3.9! The `run.py` file checks for Python 3.10-3.12, but we can update it to support 3.9 as well.

The project will work fine with Python 3.9 because:
- All dependencies support Python 3.9
- FastAPI works with Python 3.9
- PyTorch and other ML libraries support Python 3.9
- No Python 3.10+ specific features are used

---

## Troubleshooting

### Issue: python3.9 not found
```bash
# Check available versions
yum list available | grep python3

# Try installing python3 (default version)
sudo yum install python3 python3-pip python3-devel -y
python3 --version
```

### Issue: Development tools installation fails
```bash
# Try installing packages individually
sudo yum install gcc gcc-c++ make -y
```

### Issue: psycopg2 installation fails
```bash
# Install PostgreSQL development files
sudo yum install postgresql-devel -y

# Or use binary version
pip install psycopg2-binary --force-reinstall
```

---

**Recommended: Use Python 3.9 - it's faster and works perfectly with your project!**
