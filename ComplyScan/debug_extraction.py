"""Debug extraction to see what's being detected"""
import sys
sys.path.insert(0, 'f:\\Dev\\SIH\\ComplyScan')

import cv2
from pathlib import Path
from modules.ocr_engine import extract_text_from_image
from modules.extraction import extract_declarations

# Test with demo image
demo_path = Path('assets/demo_images/demo_a_compliant.png')

if demo_path.exists():
    print('=== OCR DETECTION ===')
    img = cv2.imread(str(demo_path))
    ocr_results = extract_text_from_image(img)
    
    print(f'Total text detected: {len(ocr_results)}\n')
    for r in ocr_results:
        print(f'  "{r["text"]}" (conf: {r["confidence"]:.2f})')
    
    print('\n=== EXTRACTION RESULTS ===')
    fields = extract_declarations(ocr_results)
    
    for field_name, field_data in fields.items():
        status = "✅" if field_data.get('value') else "❌"
        value = field_data.get('value') or "NOT FOUND"
        conf = field_data.get('confidence', 0)
        print(f'{status} {field_name}: {value} (conf: {conf:.2f})')
