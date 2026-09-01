"""Inspect RapidOCR API and return format"""
import sys
sys.path.insert(0, 'f:\\Dev\\SIH\\ComplyScan')

from rapidocr_onnxruntime import RapidOCR
import cv2
from pathlib import Path

# Load demo image
demo_path = Path('assets/demo_images/demo_a_compliant.png')

if demo_path.exists():
    img = cv2.imread(str(demo_path))
    ocr = RapidOCR()
    result = ocr(img)
    
    print(f"Result type: {type(result)}")
    print(f"Result length: {len(result) if result else 0}")
    
    if result and len(result) > 0:
        print(f"\nFirst detection type: {type(result[0])}")
        print(f"First detection: {result[0]}")
        print(f"First detection length: {len(result[0])}")
        
        if len(result[0]) >= 1:
            print(f"\nDetection structure:")
            for i, item in enumerate(result[0]):
                print(f"  [{i}] type={type(item)}, len={len(item) if isinstance(item, (list, tuple)) else 'N/A'}")
                if isinstance(item, (list, tuple)):
                    print(f"      content: {item}")
