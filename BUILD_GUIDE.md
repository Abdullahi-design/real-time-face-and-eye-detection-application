# Build Guide: Real-Time Face & Eye Detection System

This guide provides step-by-step instructions to build the complete face and eye detection system from scratch.

## Prerequisites Checklist

- [ ] Windows/Linux/macOS operating system
- [ ] Administrator/root access (for installations)
- [ ] Internet connection (for downloads)
- [ ] Webcam/camera device
- [ ] 2GB+ free disk space

---

## Phase 1: Environment Setup

### Step 1.1: Install Python 3.11

**Windows:**
1. Download Python 3.11 from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ **CRITICAL:** Check "Add Python to PATH"
4. Verify installation:
   ```bash
   python --version
   ```
   Expected: `Python 3.11.x`

**Linux:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-pip
python3.11 --version
```

**macOS:**
```bash
brew install python@3.11
python3.11 --version
```

### Step 1.2: Install Visual Studio Code

1. Download from [code.visualstudio.com](https://code.visualstudio.com/)
2. Install with default settings
3. Install Python extension:
   - Open VS Code
   - Extensions (Ctrl+Shift+X)
   - Search "Python"
   - Install official Python extension

### Step 1.3: Verify PIP Installation

```bash
python -m pip --version
```

If version < 23.3, upgrade:
```bash
python -m pip install --upgrade pip
```

Verify:
```bash
pip --version
```
Expected: `pip 23.3.x` or higher

---

## Phase 2: Project Setup

### Step 2.1: Create Project Folder

**Windows:**
```bash
mkdir ai-face-detection-algo
cd ai-face-detection-algo
```

**Linux/macOS:**
```bash
mkdir -p ~/ai-face-detection-algo
cd ~/ai-face-detection-algo
```

### Step 2.2: Create Project Structure

```bash
# Create main files
touch main.py
touch requirements.txt
touch README.md
touch .gitignore
```

### Step 2.3: Initialize Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3.11 -m venv venv
source venv/bin/activate
```

**Verify activation:**
- Prompt should show `(venv)`
- Check: `which python` should point to venv

---

## Phase 3: Install Dependencies

### Step 3.1: Create requirements.txt

Create `requirements.txt` with:
```
opencv-python==4.8.1.78
numpy==1.24.3
```

### Step 3.2: Install Libraries

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Verify installations:**
```bash
pip show opencv-python
pip show numpy
```

Expected outputs:
- opencv-python: `Version: 4.8.1.78`
- numpy: `Version: 1.24.3`

---

## Phase 4: Download Haar Cascades

### Step 4.1: Locate OpenCV Data

Cascades are included with OpenCV. Find them:

**Windows:**
```
C:\Users\<username>\AppData\Local\Programs\Python\Python311\Lib\site-packages\cv2\data\
```

**Linux:**
```bash
python -c "import cv2; print(cv2.__file__)"
# Navigate to: <path>/cv2/data/
```

**macOS:**
```bash
python -c "import cv2; print(cv2.__file__)"
# Navigate to: <path>/cv2/data/
```

### Step 4.2: Copy Cascade Files

Copy these files to project root:
- `haarcascade_frontalface_default.xml`
- `haarcascade_eye.xml`

**Or use Python to locate:**
```python
import cv2
import os
print(os.path.dirname(cv2.__file__) + '/data/')
```

---

## Phase 5: Implementation

### Step 5.1: Create main.py Structure

```python
# Import statements
import cv2
import numpy as np
from collections import deque
import time
import os

# Constants
FACE_CASCADE_PATH = 'haarcascade_frontalface_default.xml'
EYE_CASCADE_PATH = 'haarcascade_eye.xml'
SCREENSHOT_PATH = 'detection_screenshot.jpg'

# Performance settings
TARGET_FPS = 20
DETECTION_SCALE = 0.5  # Process at 50% resolution for speed
```

### Step 5.2: Implement Core Functions

**5.2.1: Initialize System**
```python
def initialize_system():
    # Load cascades
    # Initialize camera
    # Setup FPS calculator
    # Return initialized objects
```

**5.2.2: Frame Processing**
```python
def process_frame(frame, face_cascade, eye_cascade):
    # Resize for detection
    # Convert to grayscale
    # Detect faces
    # Detect eyes in face ROIs
    # Return detections
```

**5.2.3: Render Frame**
```python
def render_frame(frame, faces, eyes, stats):
    # Draw face rectangles (green)
    # Draw eye rectangles (blue)
    # Display statistics
    # Show FPS
```

**5.2.4: FPS Calculation**
```python
def calculate_fps(fps_queue, start_time):
    # Add frame time to queue
    # Calculate average
    # Return FPS value
```

### Step 5.3: Main Loop Implementation

```python
def main():
    # Initialize
    # Main loop:
    #   - Capture frame
    #   - Process frame
    #   - Render frame
    #   - Handle keyboard
    #   - Update FPS
    # Cleanup
```

---

## Phase 6: Optimization for 20+ FPS

### Optimization 1: Adaptive Resolution

```python
# Process at lower resolution
detection_frame = cv2.resize(frame, None, fx=DETECTION_SCALE, fy=DETECTION_SCALE)
gray = cv2.cvtColor(detection_frame, cv2.COLOR_BGR2GRAY)

# Scale coordinates back
faces = [(int(x/DETECTION_SCALE), int(y/DETECTION_SCALE), 
          int(w/DETECTION_SCALE), int(h/DETECTION_SCALE)) 
         for (x, y, w, h) in faces]
```

### Optimization 2: Efficient Cascade Parameters

```python
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,      # Balance speed/accuracy
    minNeighbors=5,       # Reduce false positives
    minSize=(30, 30),     # Skip tiny faces
    flags=cv2.CASCADE_SCALE_IMAGE
)
```

### Optimization 3: ROI-Based Eye Detection

```python
# Only process face regions
for (x, y, w, h) in faces:
    roi_gray = gray[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray, ...)
    # Adjust eye coordinates relative to full frame
```

### Optimization 4: Efficient FPS Calculation

```python
fps_queue = deque(maxlen=30)  # Last 30 frames
frame_times = []
start = time.time()
# ... process frame ...
fps_queue.append(time.time() - start)
fps = len(fps_queue) / sum(fps_queue)
```

### Optimization 5: Minimize Drawing Operations

```python
# Batch all drawing operations
# Use efficient OpenCV functions
# Update text only when values change
```

---

## Phase 7: Keyboard Controls

### Step 7.1: Implement 'q' Key (Quit)

```python
key = cv2.waitKey(1) & 0xFF
if key == ord('q'):
    break  # Exit loop
```

### Step 7.2: Implement 's' Key (Screenshot)

```python
if key == ord('s'):
    cv2.imwrite(SCREENSHOT_PATH, frame)
    print(f"Screenshot saved: {SCREENSHOT_PATH}")
```

---

## Phase 8: Error Handling

### Step 8.1: Camera Initialization

```python
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera")
    print("Troubleshooting:")
    print("1. Check camera is connected")
    print("2. Close other applications using camera")
    print("3. Try different camera index (0, 1, 2...)")
    exit(1)
```

### Step 8.2: Cascade Loading

```python
try:
    face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
    if face_cascade.empty():
        raise ValueError("Could not load face cascade")
except Exception as e:
    print(f"Error loading cascade: {e}")
    exit(1)
```

### Step 8.3: Graceful Cleanup

```python
finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Application closed successfully")
```

---

## Phase 9: Testing & Verification

### Step 9.1: Basic Functionality Test

```bash
python main.py
```

**Checklist:**
- [ ] Webcam feed appears
- [ ] Face detection works (green rectangles)
- [ ] Eye detection works (blue rectangles)
- [ ] FPS displays (should be 20+)
- [ ] 'q' key closes application
- [ ] 's' key saves screenshot

### Step 9.2: Performance Test

Run for 30 seconds and verify:
- FPS consistently > 20
- No crashes or errors
- Smooth video feed
- Accurate detection

### Step 9.3: Multi-Face Test

Test with multiple people:
- [ ] Detects up to 5 faces
- [ ] Counts faces correctly
- [ ] Counts eyes correctly
- [ ] Performance remains stable

### Step 9.4: Error Handling Test

- [ ] Close camera manually → graceful exit
- [ ] Cover camera → no crash
- [ ] No faces → displays correctly

---

## Phase 10: Final Verification

### Step 10.1: File Structure Check

```bash
ls -la
```

Should contain:
- [ ] `main.py`
- [ ] `requirements.txt`
- [ ] `venv/` folder
- [ ] `detection_screenshot.jpg` (after taking screenshot)
- [ ] `README.md`
- [ ] Cascade XML files

### Step 10.2: Command Verification

```bash
# Python version
python --version
# Expected: Python 3.11.x

# PIP version
pip --version
# Expected: pip 23.3.x or higher

# OpenCV version
python -c "import cv2; print(cv2.__version__)"
# Expected: 4.8.1.78

# NumPy version
python -c "import numpy; print(numpy.__version__)"
# Expected: 1.24.3
```

### Step 10.3: Virtual Environment Check

```bash
# Should show venv path
which python
echo $VIRTUAL_ENV  # Linux/macOS
echo %VIRTUAL_ENV%  # Windows
```

---

## Troubleshooting

### Issue: Camera not opening

**Solutions:**
1. Check camera permissions
2. Close other apps using camera
3. Try different camera index: `cv2.VideoCapture(1)`
4. Check device manager (Windows) or `ls /dev/video*` (Linux)

### Issue: Low FPS (< 20)

**Solutions:**
1. Reduce detection resolution further
2. Increase `scaleFactor` to 1.2
3. Increase `minSize` to (50, 50)
4. Close other applications
5. Check CPU usage

### Issue: Cascade files not found

**Solutions:**
1. Verify files are in project root
2. Check file paths in code
3. Use absolute paths if needed
4. Reinstall opencv-python

### Issue: Import errors

**Solutions:**
1. Verify virtual environment is activated
2. Reinstall: `pip install -r requirements.txt --force-reinstall`
3. Check Python version compatibility

---

## Performance Optimization Checklist

- [ ] Using lower resolution for detection
- [ ] Processing only face ROIs for eyes
- [ ] Optimized cascade parameters
- [ ] Efficient FPS calculation
- [ ] Minimal drawing operations
- [ ] Proper memory management
- [ ] No unnecessary frame copies

---

## Next Steps

After completing this guide:
1. Test all functionality
2. Take screenshots for submission
3. Complete score card
4. Document any bonus features
5. Prepare for demonstration

---

## Build Time Estimate

- Environment Setup: 15-30 minutes
- Project Setup: 10 minutes
- Implementation: 1-2 hours
- Testing & Optimization: 30-60 minutes
- **Total: 2-4 hours**

---

## Success Criteria

✅ Application runs without errors  
✅ FPS consistently > 20  
✅ Face detection accuracy > 90%  
✅ Eye detection accuracy > 85%  
✅ All keyboard controls work  
✅ Professional UI display  
✅ Graceful error handling  
✅ All files present and correct  
