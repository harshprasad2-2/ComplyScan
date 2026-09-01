"""Test OCR with actual demo images"""
import sys
sys.path.insert(0, 'f:\\Dev\\SIH\\ComplyScan')

import cv2
from pathlib import Path
from rapidocr_onnxruntime import RapidOCR

# Load demo image
demo_path = Path('assets/demo_images/demo_a_compliant.png')

if demo_path.exists():
    print(f'✅ Found: {demo_path}')
    img = cv2.imread(str(demo_path))
    print(f'   Image shape: {img.shape}')
    print(f'   Image dtype: {img.dtype}')
    
    # Test direct RapidOCR
    print('\nTesting RapidOCR directly...')
    ocr = RapidOCR()
    result = ocr(img)
    
    if result:
        print(f'✅ Detected {len(result)} text regions')
        for i, detection in enumerate(result[:5]):
            if len(detection) == 3:
                bbox, text, conf = detection
                print(f'   [{i}] "{text}" (conf: {conf:.2f})')
    else:
        print('❌ No text detected')
        
    # Try with grayscale
    print('\nTesting with grayscale...')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result_gray = ocr(gray)
    if result_gray:
        print(f'✅ Grayscale: Detected {len(result_gray)} regions')
        for i, detection in enumerate(result_gray[:5]):
            if len(detection) == 3:
                bbox, text, conf = detection
                print(f'   [{i}] "{text}" (conf: {conf:.2f})')
else:
    print(f'❌ Demo image not found: {demo_path}')
    print('Available demo images:')
    demo_dir = Path('assets/demo_images')
    if demo_dir.exists():
        for f in demo_dir.glob('*.png'):
            print(f'   - {f.name}')
