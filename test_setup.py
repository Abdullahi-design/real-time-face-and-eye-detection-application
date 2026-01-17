#!/usr/bin/env python3
"""
Quick setup verification script
Tests if all dependencies and camera are working
"""

import sys

print("=" * 60)
print("Setup Verification Test")
print("=" * 60)

# Test 1: Python version
print("\n[1/5] Checking Python version...")
print(f"   Python: {sys.version}")
if sys.version_info >= (3, 11):
    print("   ✓ Python version OK")
else:
    print("   ⚠ Warning: Python 3.11+ recommended")

# Test 2: OpenCV
print("\n[2/5] Checking OpenCV...")
try:
    import cv2
    print(f"   OpenCV version: {cv2.__version__}")
    print("   ✓ OpenCV installed")
except ImportError:
    print("   ❌ OpenCV not found!")
    sys.exit(1)

# Test 3: NumPy
print("\n[3/5] Checking NumPy...")
try:
    import numpy as np
    print(f"   NumPy version: {np.__version__}")
    print("   ✓ NumPy installed")
except ImportError:
    print("   ❌ NumPy not found!")
    sys.exit(1)

# Test 4: Cascade files
print("\n[4/5] Checking Haar cascade files...")
import os
cascade_dir = os.path.join(os.path.dirname(cv2.__file__), 'data')
face_cascade_path = os.path.join(cascade_dir, 'haarcascade_frontalface_default.xml')
eye_cascade_path = os.path.join(cascade_dir, 'haarcascade_eye.xml')

if os.path.exists(face_cascade_path):
    print(f"   ✓ Face cascade found: {face_cascade_path}")
else:
    print(f"   ⚠ Face cascade not found at: {face_cascade_path}")

if os.path.exists(eye_cascade_path):
    print(f"   ✓ Eye cascade found: {eye_cascade_path}")
else:
    print(f"   ⚠ Eye cascade not found at: {eye_cascade_path}")

# Test 5: Camera
print("\n[5/5] Checking camera...")
cap = cv2.VideoCapture(0)
if cap.isOpened():
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"   ✓ Camera available: {width}x{height}")
    cap.release()
else:
    print("   ⚠ Camera not accessible (may still work if other app is using it)")

print("\n" + "=" * 60)
print("Setup verification complete!")
print("=" * 60)
print("\nYou can now run: python main.py")
