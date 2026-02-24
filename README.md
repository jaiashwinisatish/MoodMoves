# AI Stickman Dancing Game...

An interactive real-time stickman game that combines Natural Language Processing (NLP) and Computer Vision to create an engaging dancing experience.

## 🎮 Game Overview

The AI Stickman Dancing Game analyzes text input using NLP to determine dance styles and uses hand gesture recognition to control the stickman character's movement. The stickman performs different dances based on sentiment analysis and keyword detection from user text.

## ✨ Features

### 🧠 NLP Features
- **Sentiment Analysis**: Uses NLTK VADER analyzer to detect positive, negative, and neutral sentiments
- **Keyword Detection**: Identifies dance-related keywords like "party", "love", "angry"
- **Dance Style Mapping**: Maps emotions and keywords to specific dance animations

### 👁️ Computer Vision Features
- **Hand Gesture Recognition**: Uses MediaPipe for real-time hand detection
- **Finger Counting**: Accurately counts raised fingers (1-5)
- **Gesture Control**: Maps finger counts to game actions

### 🎭 Dance Styles
- **Normal**: Balanced, casual dance movements
- **Happy**: Energetic and joyful dance with upbeat movements
- **Sad**: Slow, melancholic dance with gentle swaying
- **Breakdance**: Dynamic dance with acrobatic moves
- **Romantic**: Graceful and flowing romantic dance
- **Aggressive**: Intense and powerful dance with strong movements

### 🎮 Controls
- **1 Finger**: Stickman idle
- **2 Fingers**: Move stickman right
- **3 Fingers**: Move stickman left
- **5 Fingers**: Trigger special dance
- **Text Input**: Type sentences to change dance style based on sentiment

## 🏗️ Architecture

### Module Structure
```
├── main.py              # Main game loop and integration
├── nlp_engine.py        # Natural Language Processing
├── vision_engine.py     # Computer Vision and gesture detection
├── stickman.py          # Stickman character rendering
├── animations.py        # Animation system and dance patterns
├── utils.py             # Utility functions and constants
└── requirements.txt     # Python dependencies
```

### System Components

#### NLP Engine (`nlp_engine.py`)
- VADER sentiment analysis
- Keyword extraction and matching
- Dance style determination
- Text processing pipeline

#### Vision Engine (`vision_engine.py`)
- MediaPipe hand detection
- Finger counting algorithm
- Gesture smoothing and filtering
- Real-time processing

#### Stickman (`stickman.py`)
- Character rendering with OpenCV
- Animation integration
- Movement and positioning
- Visual effects

#### Animation System (`animations.py`)
- Dance pattern definitions
- Smooth transitions
- Special effects
- Time-based animations

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- Webcam or camera device
- Git (for cloning)

### Setup Instructions

1. **Clone or Download the Project**
   ```bash
   # If using git
   git clone <repository-url>
   cd "Stickman Dancing Game"
   
   # Or download and extract the ZIP file
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   # Test individual modules
   python nlp_engine.py
   python vision_engine.py
   python stickman.py
   python animations.py
   ```

## 🎯 How to Run

### Starting the Game
```bash
python main.py
```

### Game Flow
1. **Camera Setup**: The game will automatically access your webcam
2. **Text Input**: Type any text and press Enter to analyze sentiment
3. **Hand Gestures**: Use hand gestures to control stickman movement
4. **Dance**: Watch the stickman dance based on your text's emotion!

### Controls Reference
| Gesture | Action | Description |
|---------|--------|-------------|
| 1 Finger | Idle | Stickman stops moving |
| 2 Fingers | Move Right | Stickman walks right |
| 3 Fingers | Move Left | Stickman walks left |
| 5 Fingers | Special Dance | Triggers breakdance mode |
| Text Input | Change Dance | Analyzes sentiment for dance style |

## 📝 Text Input Examples

Try these text inputs to see different dance styles:

```text
"I am so happy today!"           # Happy dance
"I feel very sad and lonely"     # Sad dance
"Let's have a party tonight!"    # Breakdance
"I love you so much"             # Romantic dance
"I am angry about this"          # Aggressive dance
"Just a normal day"              # Normal dance
```

## 🔧 Configuration

### Camera Settings
Modify camera properties in `main.py`:
```python
self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
self.cap.set(cv2.CAP_PROP_FPS, FPS)
```

### Animation Settings
Adjust animation parameters in `utils.py`:
```python
ANIMATION_SPEED = 0.15      # Animation speed multiplier
DANCE_AMPLITUDE = 30        # Movement amplitude
WALK_SPEED = 5              # Character movement speed
```

### Gesture Recognition
Fine-tune gesture detection in `vision_engine.py`:
```python
min_detection_confidence=0.7  # Hand detection confidence
min_tracking_confidence=0.5   # Hand tracking confidence
```

## 🐛 Troubleshooting

### Common Issues

#### Camera Not Working
```bash
# Check camera permissions
# Ensure no other app is using the camera
# Try different camera indices (0, 1, 2...)
```

#### NLTK Download Issues
```bash
# Manually download NLTK data
python -c "import nltk; nltk.download('vader_lexicon')"
```

#### MediaPipe Installation
```bash
# If MediaPipe fails, try:
pip install mediapipe==0.10.7
# Or use CPU-only version
pip install mediapipe-silicon
```

#### Performance Issues
- Reduce camera resolution
- Lower FPS settings
- Close other applications

### Error Messages

#### "Cannot open webcam"
- Check camera connection
- Verify camera permissions
- Try different camera index

#### "NLTK download failed"
- Check internet connection
- Manually download VADER lexicon
- Use offline NLTK data

#### "MediaPipe initialization failed"
- Update MediaPipe version
- Check system compatibility
- Install CPU-only version if needed

## 🧪 Testing

### Run Individual Tests
```bash
# Test NLP engine
python nlp_engine.py

# Test vision engine (requires camera)
python vision_engine.py

# Test stickman animations
python stickman.py

# Test animation system
python animations.py
```

### Integration Test
```bash
# Full game test
python main.py
```

## 🎨 Customization

### Adding New Dance Styles
1. Add dance pattern in `animations.py`
2. Update keyword mappings in `utils.py`
3. Add visual effects in `stickman.py`

### Modifying Gesture Controls
1. Update `FINGER_GESTURES` in `utils.py`
2. Modify gesture handling in `main.py`
3. Adjust finger counting in `vision_engine.py`

### Custom Visual Effects
1. Extend particle system in `animations.py`
2. Add new drawing methods in `stickman.py`
3. Create new color schemes in `utils.py`

## 📚 Technical Details

### NLP Pipeline
1. **Text Input**: User enters text
2. **Preprocessing**: Clean and tokenize text
3. **Sentiment Analysis**: VADER sentiment scoring
4. **Keyword Detection**: Pattern matching
5. **Dance Mapping**: Sentiment/keyword to dance style

### Computer Vision Pipeline
1. **Frame Capture**: Webcam input
2. **Hand Detection**: MediaPipe processing
3. **Landmark Extraction**: Key point identification
4. **Finger Counting**: Geometric analysis
5. **Gesture Mapping**: Finger count to action

### Animation Pipeline
1. **Time Update**: Delta time calculation
2. **Pattern Selection**: Dance style parameters
3. **Offset Calculation**: Trigonometric functions
4. **Position Update**: Body part positioning
5. **Rendering**: OpenCV drawing operations

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd "Stickman Dancing Game"

# Create development environment
python -m venv dev-env
source dev-env/bin/activate  # or dev-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Code Style
- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings to functions
- Include error handling

### Testing
- Test all modules individually
- Verify integration functionality
- Check camera compatibility
- Test with various text inputs

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **NLTK**: Natural Language Toolkit for sentiment analysis
- **MediaPipe**: Google's hand tracking solution
- **OpenCV**: Computer vision library
- **NumPy**: Numerical computing support

