"""Test fixed OCR module"""
import sys
sys.path.insert(0, 'f:\\Dev\\SIH\\ComplyScan')

import cv2
from pathlib import Path
from modules.ocr_engine import extract_text_from_image

# Load demo image
demo_path = Path('assets/demo_images/demo_a_compliant.png')

if demo_path.exists():
    print(f'✅ Testing: {demo_path}')
    img = cv2.imread(str(demo_path))
    
    results = extract_text_from_image(img)
    print(f'✅ Detected {len(results)} text regions\n')
    
    for i, detection in enumerate(results[:8]):
        print(f'[{i}] "{detection["text"]}" (conf: {detection["confidence"]:.2f})')
else:
    print(f'❌ Demo image not found')
