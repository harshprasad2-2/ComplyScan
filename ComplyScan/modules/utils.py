"""
ComplyScan Utility Functions
Helper functions for common operations.
"""

import uuid
from datetime import datetime
from pathlib import Path
import json

def generate_scan_id() -> str:
    """Generate a unique scan ID."""
    return str(uuid.uuid4())[:8]

def get_timestamp() -> str:
    """Get current timestamp in standardized format."""
    return datetime.now().isoformat()

def get_readable_timestamp() -> str:
    """Get current timestamp in human-readable format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_confidence(confidence: float) -> str:
    """Format confidence as percentage."""
    return f"{confidence * 100:.1f}%"

def save_json(data: dict, filepath: str) -> None:
    """Save data as JSON file."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def load_json(filepath: str) -> dict:
    """Load data from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length with ellipsis."""
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    return text

def normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    return text.lower().strip()

def is_valid_image_file(filepath: str) -> bool:
    """Check if file is a valid image."""
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    return Path(filepath).suffix.lower() in valid_extensions

def format_rule_explanation(rule_result: dict) -> str:
    """Format rule result for display."""
    status = rule_result.get('status', 'UNKNOWN')
    explanation = rule_result.get('explanation', '')
    
    if status == 'PASS':
        return f"✅ {explanation}"
    elif status == 'FAIL':
        return f"❌ {explanation}"
    else:  # REVIEW
        return f"⚠️ {explanation}"

def create_evidence_summary(rule_results: list) -> str:
    """Create a text summary of evidence."""
    summary = []
    for rule in rule_results:
        summary.append(format_rule_explanation(rule))
    return "\n".join(summary)
