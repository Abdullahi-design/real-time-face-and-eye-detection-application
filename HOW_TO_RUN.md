# How to Run - Face & Eye Detection System

A quick guide to get the application running in minutes.

## Prerequisites

- Python 3.11+ installed
- Webcam/camera connected
- Internet connection (for first-time setup)

## Quick Start (3 Steps)

### Step 1: Activate Virtual Environment

```bash
source venv/bin/activate
```

**Windows users:**
```bash
venv\Scripts\activate
```

### Step 2: Install Dependencies (First Time Only)

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python main.py
```

That's it! The application will start automatically.

---

## What to Expect

1. **Startup**: Console messages showing initialization progress
2. **Camera Window**: A window opens showing your webcam feed
3. **Detection**: 
   - 🟢 **Green rectangles** = Detected faces
   - 🔵 **Blue rectangles** = Detected eyes
4. **Statistics**: Top-left corner shows:
   - Face count
   - Eye count
   - FPS (should be 20+)
   - Processing time

---

## Controls

| Key | Action |
|-----|--------|
| `q` | Quit application |
| `s` | Save screenshot |

---

## Troubleshooting

### Camera Not Opening?
- Close other applications using the camera
- Check camera permissions
- Try a different camera index in code (0, 1, 2...)

### Low FPS?
- Ensure good lighting
- Close other resource-intensive apps
- The app is optimized for 20+ FPS

### Import Errors?
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

---

## Verification

To verify everything is set up correctly:

```bash
python test_setup.py
```

This will check:
- ✓ Python version
- ✓ OpenCV installation
- ✓ NumPy installation
- ✓ Cascade files
- ✓ Camera availability

---

## Need More Help?

- See [README.md](README.md) for detailed documentation
- See [BUILD_GUIDE.md](BUILD_GUIDE.md) for complete setup instructions
- See [ARCHITECTURE.md](ARCHITECTURE.md) for technical details

---

**Happy Detecting! 🎯**
