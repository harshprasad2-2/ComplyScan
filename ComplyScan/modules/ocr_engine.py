"""
ComplyScan OCR Engine Module
Handles optical character recognition using RapidOCR.
"""

import cv2
import numpy as np
from pathlib import Path

try:
    from rapidocr_onnxruntime import RapidOCR
    RAPIDOCR_AVAILABLE = True
except ImportError:
    RAPIDOCR_AVAILABLE = False

class OCRProvider:
    """Abstract OCR provider interface."""
    
    def extract_text(self, image):
        """Extract text from image. Returns list of (text, confidence, bbox) tuples."""
        raise NotImplementedError

class RapidOCRProvider(OCRProvider):
    """RapidOCR implementation for local text extraction."""
    
    def __init__(self):
        if not RAPIDOCR_AVAILABLE:
            raise ImportError("RapidOCR not available. Install: pip install rapidocr-onnxruntime")
        self.ocr = RapidOCR()
    
    def extract_text(self, image):
        """
        Extract text from image using RapidOCR.
        
        Args:
            image (np.ndarray): Input image (BGR or grayscale)
        
        Returns:
            list: List of dicts with keys: text, confidence, bbox
        """
        if len(image.shape) == 2:
            # Convert grayscale to BGR
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        try:
            result = self.ocr(image)
            
            # RapidOCR returns (detections_list, timing_info)
            if not result or not result[0]:
                return []
            
            detections = result[0]  # Get the list of detections
            ocr_results = []
            
            for detection in detections:
                # Each detection is [bbox_points, text, confidence_str]
                if len(detection) >= 3:
                    bbox_points = detection[0]
                    text = detection[1]
                    confidence_str = detection[2]
                    
                    # Convert confidence string to float
                    confidence = float(confidence_str)
                    
                    # Convert polygon points to axis-aligned bounding box
                    points = np.array(bbox_points, dtype=np.int32)
                    x_min = int(np.min(points[:, 0]))
                    y_min = int(np.min(points[:, 1]))
                    x_max = int(np.max(points[:, 0]))
                    y_max = int(np.max(points[:, 1]))
                    
                    ocr_results.append({
                        'text': text.strip(),
                        'confidence': confidence,
                        'bbox': (x_min, y_min, x_max - x_min, y_max - y_min),
                        'bbox_points': bbox_points
                    })
            
            return ocr_results
        
        except Exception as e:
            print(f"OCR Error: {e}")
            return []
            
            return ocr_results
        
        except Exception as e:
            print(f"OCR Error: {e}")
            return []

class FallbackOCRProvider(OCRProvider):
    """Fallback mock OCR for testing without RapidOCR."""
    
    def extract_text(self, image):
        """Return empty results (for testing)."""
        return []

def get_ocr_provider():
    """Get the appropriate OCR provider."""
    if RAPIDOCR_AVAILABLE:
        try:
            return RapidOCRProvider()
        except Exception as e:
            print(f"Failed to initialize RapidOCR: {e}. Using fallback.")
            return FallbackOCRProvider()
    else:
        print("RapidOCR not installed. Using fallback (no text extraction).")
        return FallbackOCRProvider()

def extract_text_from_image(image):
    """
    Convenience function to extract text from an image.
    
    Args:
        image (np.ndarray): Input image (BGR, RGB, or grayscale)
    
    Returns:
        list: List of text detections with confidence and position
    """
    # Improve binary/threshold images before OCR
    if len(image.shape) == 2:  # Grayscale image
        # Check if image is too binary (almost all black/white)
        unique_vals = len(np.unique(image))
        if unique_vals < 10:  # Very binary
            # Enhance contrast for OCR
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            image = clahe.apply(image)
        
        # Convert to BGR for RapidOCR
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    provider = get_ocr_provider()
    return provider.extract_text(image)

def extract_text_from_file(image_path):
    """Extract text from an image file."""
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Could not load image from {image_path}")
    
    return extract_text_from_image(image)
