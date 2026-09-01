"""
ComplyScan Image Processing Module
Handles image preprocessing using OpenCV to improve OCR accuracy.
"""

import cv2
import numpy as np
from pathlib import Path
from modules.config import MAX_IMAGE_SIZE

def load_image(image_path):
    """Load an image from file."""
    if isinstance(image_path, str):
        image_path = Path(image_path)
    
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not load image from {image_path}")
    return img

def _deskew_image(image, angle_threshold=3.0):
    """
    Attempt to correct rotation/skew in image.
    Uses edge detection and Hough line transform.
    """
    try:
        # Use Canny edge detection
        edges = cv2.Canny(image, 50, 150)
        
        # Use Hough line transform to detect lines
        lines = cv2.HoughLines(edges, 1, np.pi/180, 50)
        
        if lines is not None and len(lines) > 0:
            # Calculate average angle
            angles = []
            for line in lines[:10]:  # Use first 10 lines
                rho, theta = line[0]
                angle = np.degrees(theta) - 90
                if abs(angle) > angle_threshold:
                    angles.append(angle)
            
            if angles:
                avg_angle = np.median(angles)
                
                # Rotate image to correct skew
                h, w = image.shape[:2]
                center = (w // 2, h // 2)
                rot_matrix = cv2.getRotationMatrix2D(center, avg_angle, 1.0)
                rotated = cv2.warpAffine(image, rot_matrix, (w, h), 
                                        borderMode=cv2.BORDER_REPLICATE)
                return rotated
    except:
        pass
    
    return image

def preprocess_image(image):
    """
    Preprocess image for better OCR accuracy.
    
    Steps:
    1. Resize if too large
    2. Convert to grayscale
    3. Attempt deskew/rotation correction
    4. Apply denoising
    5. Enhance contrast
    6. Apply adaptive thresholding
    """
    # Resize if image is too large
    h, w = image.shape[:2]
    if w > MAX_IMAGE_SIZE[0] or h > MAX_IMAGE_SIZE[1]:
        scale = min(MAX_IMAGE_SIZE[0] / w, MAX_IMAGE_SIZE[1] / h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    # Convert to grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Attempt deskew/rotation correction
    gray = _deskew_image(gray)
    
    # Apply denoising
    denoised = cv2.fastNlMeansDenoising(gray, h=10, templateWindowSize=7, searchWindowSize=21)
    
    # Enhance contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoised)
    
    # Apply adaptive thresholding for better text visibility
    thresh = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)
    
    return thresh, enhanced, gray

def detect_text_regions(image):
    """
    Detect regions containing text using contour detection.
    Returns bounding boxes of potential text regions.
    """
    # Apply morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated = cv2.dilate(image, kernel, iterations=2)
    
    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours by size (remove too small/large)
    h, w = image.shape[:2]
    min_area = (w * h) * 0.001  # 0.1% of image area
    max_area = (w * h) * 0.7    # 70% of image area
    
    text_regions = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area < area < max_area:
            x, y, bw, bh = cv2.boundingRect(contour)
            text_regions.append((x, y, bw, bh))
    
    return text_regions

def draw_evidence_boxes(image_path, ocr_results):
    """
    Draw bounding boxes around detected text for evidence visualization.
    
    Args:
        image_path (str): Path to original image
        ocr_results (list): List of OCR results with bounding boxes
    
    Returns:
        np.ndarray: Image with drawn boxes
    """
    image = load_image(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    for result in ocr_results:
        if 'bbox' in result:
            x, y, w, h = result['bbox']
            # Draw green rectangle around detected text
            cv2.rectangle(image_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Add field label
            if 'field' in result:
                label = result['field']
                confidence = result.get('confidence', 0)
                text = f"{label} ({confidence:.1%})"
                cv2.putText(image_rgb, text, (x, y - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    return image_rgb

def crop_region(image, x, y, w, h):
    """Crop a region from image."""
    return image[y:y+h, x:x+w]

def save_processed_image(image, output_path):
    """Save processed image to file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if len(image.shape) == 3 and image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    cv2.imwrite(str(output_path), image)
    return str(output_path)
