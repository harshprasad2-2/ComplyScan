"""Test RapidOCR functionality"""
import sys
sys.path.insert(0, 'f:\\Dev\\SIH\\ComplyScan')

from rapidocr_onnxruntime import RapidOCR
import cv2
import numpy as np
from modules.image_processing import preprocess_image

print("Testing RapidOCR...")

# Test 1: Simple text detection
print("\n1. Simple Text Test:")
ocr = RapidOCR()
img = np.ones((100, 300, 3), dtype=np.uint8) * 255
cv2.putText(img, 'MANCHOW SOUP', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

result = ocr(img)
if result and len(result) > 0:
    print("✅ RapidOCR works on simple image")
    for detection in result:
        if len(detection) == 3:
            bbox, text, conf = detection
            print(f"   Text: '{text}' (conf: {conf:.2f})")
else:
    print("❌ RapidOCR failed on simple image")

# Test 2: Preprocessed image
print("\n2. Preprocessed Image Test:")
img2 = np.ones((200, 400, 3), dtype=np.uint8) * 200
cv2.putText(img2, 'NET QTY: 14g', (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 50), 2)

try:
    thresh, enhanced, gray = preprocess_image(img2)
    result2 = ocr(enhanced)
    if result2 and len(result2) > 0:
        print("✅ RapidOCR works on preprocessed image")
        for detection in result2:
            if len(detection) == 3:
                bbox, text, conf = detection
                print(f"   Text: '{text}' (conf: {conf:.2f})")
    else:
        print("❌ RapidOCR returned empty on preprocessed image")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n✅ Test complete")
