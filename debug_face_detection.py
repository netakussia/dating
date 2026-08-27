#!/usr/bin/env python3
"""Debug script to test face detection on a specific photo."""

import sys
from pathlib import Path

def test_face_detection():
    try:
        import cv2
        import numpy as np
    except ImportError as e:
        print(f"❌ Dependencies missing: {e}")
        print("Install: pip install opencv-python numpy onnxruntime")
        return

    photo_path = Path("/home/neta/dating/project1/tests/photo/Pokecut_1784476792359.jpg")
    
    if not photo_path.exists():
        print(f"❌ Photo not found: {photo_path}")
        return

    print(f"📸 Testing: {photo_path.name}")
    print(f"📏 File size: {photo_path.stat().st_size:,} bytes")
    
    # Load image
    image = cv2.imread(str(photo_path))
    if image is None:
        print("❌ Failed to load image")
        return
    
    height, width = image.shape[:2]
    print(f"📐 Image dimensions: {width}x{height}")
    
    # Test different thresholds
    model_path = Path("/models/face_detection_yunet_2023mar.onnx")
    if not model_path.exists():
        print(f"⚠️  Model not found: {model_path}")
        print("   Skipping YuNet detection test")
        return
    
    print(f"\n🧠 Testing YuNet face detector...")
    
    # Test with default settings (960 max dimension)
    test_configs = [
        {"threshold": 0.3, "max_dim": 960},
        {"threshold": 0.5, "max_dim": 960},
        {"threshold": 0.7, "max_dim": 960},
        {"threshold": 0.5, "max_dim": 1920},  # Double resolution
        {"threshold": 0.5, "max_dim": width},  # Full resolution
    ]
    
    for config in test_configs:
        threshold = config["threshold"]
        max_dim = config["max_dim"]
        
        # Calculate resize dimensions
        largest = max(width, height)
        if largest > max_dim:
            scale = max_dim / largest
            new_w, new_h = max(1, round(width * scale)), max(1, round(height * scale))
        else:
            new_w, new_h = width, height
        
        # Resize if needed
        if (new_w, new_h) != (width, height):
            test_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        else:
            test_image = image
        
        # Create detector
        detector = cv2.FaceDetectorYN.create(
            str(model_path), "", (new_w, new_h), threshold, 0.3, 5000
        )
        
        # Detect faces
        _, faces = detector.detect(test_image)
        face_count = 0 if faces is None else len(faces)
        
        status = "✅" if face_count > 0 else "❌"
        print(f"  {status} Threshold={threshold}, MaxDim={max_dim}: Resized to {new_w}x{new_h} → {face_count} face(s)")
        
        if faces is not None and len(faces) > 0:
            for i, face in enumerate(faces):
                x, y, w, h, conf = face[:5]
                print(f"     Face {i+1}: pos=({x:.0f},{y:.0f}), size={w:.0f}x{h:.0f}, confidence={conf:.3f}")

if __name__ == "__main__":
    test_face_detection()
