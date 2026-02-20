# Installation Guide

## 🚀 Quick Start

### System Requirements
- **Python**: 3.10 or higher
- **Operating System**: Windows, macOS, or Linux
- **Hardware**: Webcam or camera device
- **Memory**: Minimum 4GB RAM
- **Storage**: 500MB free space

### Step-by-Step Installation

#### 1. Download the Project
```bash
# Option A: Download ZIP
# Download the project ZIP file and extract to your desired location

# Option B: Git Clone (if available)
git clone <repository-url>
cd "Stickman Dancing Game"
```

#### 2. Set Up Python Environment
```bash
# Create virtual environment (recommended)
python -m venv stickman_env

# Activate virtual environment
# Windows:
stickman_env\Scripts\activate

# macOS/Linux:
source stickman_env/bin/activate
```

#### 3. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

#### 4. Test the Installation
```bash
# Test individual components
python nlp_engine.py      # Should run without errors
python animations.py      # Should show test output

# Test camera (optional)
python vision_engine.py   # Press 'q' to quit
```

#### 5. Run the Game
```bash
python main.py
```

## 📦 Dependencies

### Core Libraries
- **opencv-python (4.8.1.78)**: Computer vision and image processing
- **mediapipe (0.10.7)**: Hand gesture detection
- **nltk (3.8.1)**: Natural language processing
- **numpy (1.24.3)**: Numerical computations
- **pygame (2.5.2)**: Enhanced graphics support

### Installation Details

#### OpenCV
```bash
# Standard installation
pip install opencv-python==4.8.1.78

# Alternative if issues occur
pip install opencv-contrib-python==4.8.1.78
```

#### MediaPipe
```bash
# Standard installation
pip install mediapipe==0.10.7

# For systems without GPU support
pip install mediapipe-silicon==0.10.7
```

#### NLTK
```bash
# NLTK installation
pip install nltk==3.8.1

# Download required data (automatic on first run)
python -c "import nltk; nltk.download('vader_lexicon')"
```

## 🔧 Platform-Specific Instructions

### Windows
1. **Install Python 3.10+** from python.org
2. **Add Python to PATH** during installation
3. **Install Visual C++ Redistributable** if needed
4. **Run Command Prompt as Administrator** for installation

```powershell
# PowerShell commands
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
python main.py
```

### macOS
1. **Install Homebrew** (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. **Install Python**
```bash
brew install python@3.10
```

3. **Install Project**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Linux (Ubuntu/Debian)
1. **Update System**
```bash
sudo apt update && sudo apt upgrade -y
```

2. **Install Python and Dependencies**
```bash
sudo apt install python3.10 python3.10-venv python3-pip
sudo apt install libgl1-mesa-glx libglib2.0-0
```

3. **Install Project**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## 🐛 Common Installation Issues

### Issue: "Python not found"
**Solution:**
```bash
# Verify Python installation
python --version
# or
python3 --version

# Add Python to PATH (Windows)
# During Python installation, check "Add Python to PATH"
```

### Issue: "pip not found"
**Solution:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Alternative installation
python -m ensurepip --upgrade
```

### Issue: "Camera access denied"
**Solution:**
```bash
# Windows: Check camera privacy settings
# Settings > Privacy > Camera > Allow apps to access camera

# macOS: Grant camera permission
# System Preferences > Security & Privacy > Privacy > Camera

# Linux: Check camera permissions
sudo usermod -a -G video $USER
# Then logout and login again
```

### Issue: "NLTK download failed"
**Solution:**
```bash
# Manual NLTK data download
python -c "
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('vader_lexicon')
"
```

### Issue: "MediaPipe installation failed"
**Solution:**
```bash
# Try different MediaPipe versions
pip install mediapipe==0.10.3
# or
pip install mediapipe==0.9.0.1

# For ARM-based Macs
pip install mediapipe-silicon
```

### Issue: "OpenCV installation failed"
**Solution:**
```bash
# Try different OpenCV packages
pip install opencv-contrib-python
# or
pip install opencv-python-headless

# For Linux: Install system dependencies
sudo apt install libopencv-dev python3-opencv
```

## 🧪 Verification Tests

### Test 1: Python Environment
```bash
python --version
pip --version
```

### Test 2: Library Imports
```bash
python -c "
import cv2
import mediapipe as mp
import nltk
import numpy as np
import pygame
print('All libraries imported successfully!')
"
```

### Test 3: Individual Modules
```bash
# Test NLP (no camera required)
python nlp_engine.py

# Test Animations (no camera required)
python animations.py

# Test Stickman (no camera required)
python stickman.py
```

### Test 4: Camera Test
```bash
# Test camera and gesture detection
python vision_engine.py
# Press 'q' to quit
```

### Test 5: Full Game
```bash
# Run complete game
python main.py
```

## 📱 Alternative Installation Methods

### Using Conda
```bash
# Create conda environment
conda create -n stickman python=3.10
conda activate stickman

# Install packages
conda install opencv
pip install mediapipe nltk numpy pygame

# Run game
python main.py
```

### Using Docker
```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

```bash
# Build and run
docker build -t stickman-game .
docker run -it --device /dev/video0 stickman-game
```

## 🎯 First Run Setup

### Initial Configuration
1. **Allow Camera Access** when prompted
2. **Test Text Input**: Type "hello world" and press Enter
3. **Test Hand Gestures**: Show 1-5 fingers to camera
4. **Verify Dance Styles**: Try different text inputs

### Recommended First Inputs
```text
hello                    # Normal dance
I am happy!             # Happy dance
party time              # Breakdance
I love this             # Romantic dance
```

### Performance Optimization
```bash
# If game runs slowly, try:
# 1. Close other applications
# 2. Reduce camera resolution in main.py
# 3. Lower FPS settings in utils.py
```

## 📞 Getting Help

### Debug Mode
Add debug prints to identify issues:
```python
# In main.py, add:
print(f"Camera status: {self.cap.isOpened()}")
print(f"Hand detected: {gesture_result['hand_detected']}")
```

### Log Files
Check for error messages in terminal output. Common error locations:
- Camera initialization
- NLTK data download
- MediaPipe hand detection

### Community Support
- Check the README.md for troubleshooting
- Review the technical documentation
- Test individual components first

---

**Installation Complete! 🎉**

Now you're ready to enjoy the AI Stickman Dancing Game!
