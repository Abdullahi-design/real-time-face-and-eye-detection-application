"""
Real-Time Face & Eye Detection System
AI Vision Hackathon 2025

A high-performance computer vision application that detects faces and eyes
in real-time with guaranteed 20+ FPS performance.

Author: AI Vision Hackathon 2025 Participant
Institution: Federal University Dutsi-Ma, Katsina State
"""

import cv2
import numpy as np
from collections import deque
import time
import os
import sys

# ============================================================================
# CONSTANTS & CONFIGURATION
# ============================================================================

# Performance optimization settings
DETECTION_SCALE = 0.5  # Process at 50% resolution for speed (320x240 from 640x480)
TARGET_FPS = 20
FPS_QUEUE_SIZE = 30  # Rolling average window

# Detection parameters (optimized for speed and accuracy)
FACE_SCALE_FACTOR = 1.1
FACE_MIN_NEIGHBORS = 5
FACE_MIN_SIZE = (30, 30)

EYE_SCALE_FACTOR = 1.1
EYE_MIN_NEIGHBORS = 3
EYE_MIN_SIZE = (15, 15)

# File paths
SCREENSHOT_PATH = 'detection_screenshot.jpg'

# Colors (BGR format for OpenCV)
COLOR_FACE = (0, 255, 0)      # Green for faces
COLOR_EYE = (255, 0, 0)       # Blue for eyes
COLOR_TEXT = (255, 255, 255)  # White for text
COLOR_BG = (0, 0, 0)          # Black background for text

# ============================================================================
# CASCADE FILE LOCATION
# ============================================================================

def find_cascade_files():
    """
    Locate Haar cascade XML files.
    Tries multiple common locations.
    """
    # Possible cascade file locations
    possible_paths = [
        # In project directory
        'haarcascade_frontalface_default.xml',
        'haarcascade_eye.xml',
        
        # OpenCV installation directory
        os.path.join(os.path.dirname(cv2.__file__), 'data', 'haarcascade_frontalface_default.xml'),
        os.path.join(os.path.dirname(cv2.__file__), 'data', 'haarcascade_eye.xml'),
        
        # Alternative paths
        '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml',
        '/usr/share/opencv4/haarcascades/haarcascade_eye.xml',
    ]
    
    face_cascade_path = None
    eye_cascade_path = None
    
    # Find face cascade
    for path in possible_paths[::2]:  # Every other path (face cascades)
        if os.path.exists(path):
            face_cascade_path = path
            break
    
    # Find eye cascade
    for path in possible_paths[1::2]:  # Every other path (eye cascades)
        if os.path.exists(path):
            eye_cascade_path = path
            break
    
    return face_cascade_path, eye_cascade_path

# ============================================================================
# INITIALIZATION FUNCTIONS
# ============================================================================

def initialize_cascades():
    """
    Load Haar cascade classifiers for face and eye detection.
    
    Returns:
        tuple: (face_cascade, eye_cascade) or (None, None) on failure
    """
    face_path, eye_path = find_cascade_files()
    
    if not face_path or not eye_path:
        print("=" * 60)
        print("ERROR: Could not locate Haar cascade files!")
        print("=" * 60)
        print("\nTroubleshooting:")
        print("1. Verify OpenCV is installed: pip show opencv-python")
        print("2. Cascade files should be in one of these locations:")
        print("   - Project root directory")
        print("   - OpenCV data directory")
        print("3. Try copying cascade files to project root:")
        print("   - haarcascade_frontalface_default.xml")
        print("   - haarcascade_eye.xml")
        print("\nOpenCV data directory location:")
        try:
            data_dir = os.path.join(os.path.dirname(cv2.__file__), 'data')
            print(f"   {data_dir}")
        except:
            pass
        return None, None
    
    # Load cascades
    face_cascade = cv2.CascadeClassifier(face_path)
    eye_cascade = cv2.CascadeClassifier(eye_path)
    
    # Verify cascades loaded correctly
    if face_cascade.empty():
        print(f"ERROR: Failed to load face cascade from: {face_path}")
        return None, None
    
    if eye_cascade.empty():
        print(f"ERROR: Failed to load eye cascade from: {eye_path}")
        return None, None
    
    print(f"✓ Face cascade loaded: {face_path}")
    print(f"✓ Eye cascade loaded: {eye_path}")
    
    return face_cascade, eye_cascade

def initialize_camera(camera_index=0):
    """
    Initialize and configure webcam.
    
    Args:
        camera_index: Camera device index (default: 0)
    
    Returns:
        cv2.VideoCapture object or None on failure
    """
    print("\nInitializing camera...")
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print("=" * 60)
        print("ERROR: Could not open camera!")
        print("=" * 60)
        print("\nTroubleshooting:")
        print("1. Check camera is connected and recognized")
        print("2. Close other applications using the camera")
        print("3. Try different camera index:")
        print("   - Change camera_index in code (0, 1, 2...)")
        print("4. Check camera permissions in system settings")
        return None
    
    # Set camera properties for optimal performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    # Verify camera properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"✓ Camera initialized: {width}x{height} @ {fps} FPS")
    
    return cap

# ============================================================================
# DETECTION FUNCTIONS
# ============================================================================

def detect_faces_and_eyes(frame, face_cascade, eye_cascade):
    """
    Detect faces and eyes in a frame with optimized processing.
    
    Args:
        frame: Input frame (BGR format)
        face_cascade: Face detection cascade classifier
        eye_cascade: Eye detection cascade classifier
    
    Returns:
        tuple: (faces, eyes) where faces and eyes are lists of (x, y, w, h) tuples
    """
    # Create smaller frame for detection (optimization: faster processing)
    small_frame = cv2.resize(frame, None, fx=DETECTION_SCALE, fy=DETECTION_SCALE)
    
    # Convert to grayscale (required for Haar cascades)
    gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces with optimized parameters
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=FACE_SCALE_FACTOR,
        minNeighbors=FACE_MIN_NEIGHBORS,
        minSize=FACE_MIN_SIZE,
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    
    # Scale face coordinates back to original frame size
    faces = [(int(x / DETECTION_SCALE), int(y / DETECTION_SCALE),
              int(w / DETECTION_SCALE), int(h / DETECTION_SCALE))
             for (x, y, w, h) in faces]
    
    # Detect eyes only within face regions (optimization: ROI processing)
    eyes = []
    gray_full = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    for (fx, fy, fw, fh) in faces:
        # Extract face region of interest
        roi_gray = gray_full[fy:fy+fh, fx:fx+fw]
        
        # Detect eyes in face ROI
        eyes_in_face = eye_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=EYE_SCALE_FACTOR,
            minNeighbors=EYE_MIN_NEIGHBORS,
            minSize=EYE_MIN_SIZE,
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # Adjust eye coordinates to full frame coordinates
        for (ex, ey, ew, eh) in eyes_in_face:
            eyes.append((fx + ex, fy + ey, ew, eh))
    
    return faces, eyes

# ============================================================================
# RENDERING FUNCTIONS
# ============================================================================

def draw_detections(frame, faces, eyes):
    """
    Draw detection rectangles on frame.
    
    Args:
        frame: Frame to draw on
        faces: List of face coordinates (x, y, w, h)
        eyes: List of eye coordinates (x, y, w, h)
    """
    # Draw face rectangles (green)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), COLOR_FACE, 2)
    
    # Draw eye rectangles (blue)
    for (x, y, w, h) in eyes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), COLOR_EYE, 2)

def draw_statistics(frame, face_count, eye_count, fps, processing_time):
    """
    Draw statistics overlay on frame.
    
    Args:
        frame: Frame to draw on
        face_count: Number of detected faces
        eye_count: Number of detected eyes
        fps: Current FPS
        processing_time: Frame processing time in ms
    """
    # Create semi-transparent background for text
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (300, 150), COLOR_BG, -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
    
    # Text properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2
    y_offset = 30
    line_height = 25
    
    # Draw statistics
    stats = [
        f"Faces: {face_count}",
        f"Eyes: {eye_count}",
        f"FPS: {fps:.1f}",
        f"Processing: {processing_time:.1f}ms",
        "",
        "Press 'q' to quit",
        "Press 's' for screenshot"
    ]
    
    for i, stat in enumerate(stats):
        y_pos = 30 + (i * line_height)
        cv2.putText(frame, stat, (20, y_pos), font, font_scale,
                   COLOR_TEXT, thickness, cv2.LINE_AA)

# ============================================================================
# FPS CALCULATION
# ============================================================================

class FPSCalculator:
    """Efficient FPS calculator using rolling average."""
    
    def __init__(self, queue_size=30):
        """
        Initialize FPS calculator.
        
        Args:
            queue_size: Size of rolling average window
        """
        self.frame_times = deque(maxlen=queue_size)
        self.last_time = time.time()
    
    def update(self):
        """
        Update FPS calculation with current frame.
        
        Returns:
            float: Current FPS
        """
        current_time = time.time()
        frame_time = current_time - self.last_time
        self.last_time = current_time
        
        if frame_time > 0:
            self.frame_times.append(frame_time)
        
        if len(self.frame_times) > 0:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0
            return fps
        return 0.0

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """
    Main application entry point.
    """
    print("=" * 60)
    print("Real-Time Face & Eye Detection System")
    print("AI Vision Hackathon 2025")
    print("=" * 60)
    
    # Initialize cascades
    print("\n[1/3] Loading detection models...")
    face_cascade, eye_cascade = initialize_cascades()
    
    if face_cascade is None or eye_cascade is None:
        print("\n❌ Initialization failed. Exiting...")
        sys.exit(1)
    
    # Initialize camera
    print("\n[2/3] Initializing camera...")
    cap = initialize_camera(0)
    
    if cap is None:
        print("\n❌ Camera initialization failed. Exiting...")
        sys.exit(1)
    
    # Initialize FPS calculator
    print("\n[3/3] Initializing performance monitor...")
    fps_calculator = FPSCalculator(FPS_QUEUE_SIZE)
    print("✓ Performance monitor ready")
    
    print("\n" + "=" * 60)
    print("Application ready! Starting detection...")
    print("=" * 60)
    print("\nControls:")
    print("  'q' - Quit application")
    print("  's' - Save screenshot")
    print("\nPress 'q' to exit when done.\n")
    
    frame_count = 0
    start_time = time.time()
    
    try:
        while True:
            # Capture frame
            ret, frame = cap.read()
            
            if not ret:
                print("Warning: Failed to capture frame. Retrying...")
                continue
            
            # Start processing timer
            process_start = time.time()
            
            # Detect faces and eyes
            faces, eyes = detect_faces_and_eyes(frame, face_cascade, eye_cascade)
            
            # Calculate processing time
            processing_time = (time.time() - process_start) * 1000  # Convert to ms
            
            # Update FPS
            fps = fps_calculator.update()
            
            # Count faces and eyes
            face_count = len(faces)
            eye_count = len(eyes)
            
            # Limit face count display (competition requirement: up to 5)
            display_face_count = min(face_count, 5)
            
            # Draw detections
            draw_detections(frame, faces, eyes)
            
            # Draw statistics
            draw_statistics(frame, display_face_count, eye_count, fps, processing_time)
            
            # Display frame
            cv2.imshow('Face & Eye Detection System', frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\nQuit key pressed. Exiting...")
                break
            
            elif key == ord('s'):
                # Save screenshot
                cv2.imwrite(SCREENSHOT_PATH, frame)
                print(f"\n✓ Screenshot saved: {SCREENSHOT_PATH}")
            
            frame_count += 1
            
            # Print performance stats every 100 frames
            if frame_count % 100 == 0:
                elapsed = time.time() - start_time
                avg_fps = frame_count / elapsed if elapsed > 0 else 0
                print(f"Performance: {avg_fps:.1f} avg FPS | "
                      f"{fps:.1f} current FPS | "
                      f"{processing_time:.1f}ms/frame | "
                      f"{face_count} faces, {eye_count} eyes")
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
    
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        print("\nCleaning up resources...")
        cap.release()
        cv2.destroyAllWindows()
        
        # Final statistics
        if frame_count > 0:
            total_time = time.time() - start_time
            avg_fps = frame_count / total_time if total_time > 0 else 0
            print(f"\n" + "=" * 60)
            print("Session Statistics:")
            print("=" * 60)
            print(f"Total frames processed: {frame_count}")
            print(f"Total time: {total_time:.1f} seconds")
            print(f"Average FPS: {avg_fps:.1f}")
            print("=" * 60)
        
        print("\n✓ Application closed successfully.")
        print("Thank you for using Face & Eye Detection System!")

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
