"""
ComplyScan Configuration and Constants
Defines all settings, rules, and legal requirements for the MVP.
"""

import os
from pathlib import Path

# ===== APPLICATION SETTINGS =====
APP_NAME = "ComplyScan"
APP_VERSION = "1.0.0"
APP_SUBTITLE = "AI-assisted packaged commodity compliance screening"

# ===== PATHS =====
PROJECT_ROOT = Path(__file__).parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"
UPLOADS_FOLDER = PROJECT_ROOT / "uploads"
REPORTS_FOLDER = PROJECT_ROOT / "reports"
ASSETS_FOLDER = PROJECT_ROOT / "assets"
DEMO_IMAGES_FOLDER = ASSETS_FOLDER / "demo_images"

# Create folders if they don't exist
DATA_FOLDER.mkdir(exist_ok=True)
UPLOADS_FOLDER.mkdir(exist_ok=True)
REPORTS_FOLDER.mkdir(exist_ok=True)
ASSETS_FOLDER.mkdir(exist_ok=True)
DEMO_IMAGES_FOLDER.mkdir(exist_ok=True)

# ===== DATABASE SETTINGS =====
DATABASE_PATH = DATA_FOLDER / "complyscan.db"

# ===== OCR SETTINGS =====
OCR_CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for OCR text
MAX_IMAGE_SIZE = (2000, 2000)  # Max image dimensions for processing
IMAGE_QUALITY = 95  # JPEG quality for saved evidence images

# ===== COMPLIANCE RULES (Legal Metrology (Packaged Commodities) Rules, 2011) =====
# Indicative rule mapping - verify against current notified version before enforcement action

COMPLIANCE_RULES = {
    "LMPC-06-MANUFACTURER": {
        "field": "manufacturer",
        "description": "Name and address of manufacturer/packer/importer",
        "required": True,
        "check_type": "presence",
        "legal_reference": "Schedule 4, Rule 6"
    },
    "LMPC-06-COMMODITY": {
        "field": "commodity_name",
        "description": "Common or generic name of commodity",
        "required": True,
        "check_type": "presence",
        "legal_reference": "Schedule 4, Rule 6"
    },
    "LMPC-06-QTY": {
        "field": "net_quantity",
        "description": "Net quantity in standard units (weight/volume/number)",
        "required": True,
        "check_type": "regex",
        "pattern": r"(\d+(?:\.\d+)?)\s*(g|kg|ml|l|count|no\.)",
        "legal_reference": "Schedule 4, Rule 6"
    },
    "LMPC-06-DATE": {
        "field": "manufacture_or_pack_date",
        "description": "Month and year of manufacture/packing/import (MM/YYYY)",
        "required": True,
        "check_type": "date_format",
        "pattern": r"(0[1-9]|1[0-2])/\d{4}",
        "legal_reference": "Schedule 4, Rule 6"
    },
    "LMPC-06-MRP": {
        "field": "mrp",
        "description": "Maximum Retail Price (MRP)",
        "required": True,
        "check_type": "regex",
        "pattern": r"(Rs\.?|₹)\s*(\d+(?:\.\d+)?)",
        "legal_reference": "Schedule 4, Rule 6"
    },
    "LMPC-06-MRP-TAX": {
        "field": "mrp_inclusive_tax",
        "description": "MRP stated as inclusive of all taxes",
        "required": True,
        "check_type": "keyword",
        "keywords": ["inclusive of all taxes", "inclusive of tax"],
        "legal_reference": "Schedule 4, Rule 6"
    },
    "LMPC-06-CONSUMER": {
        "field": "consumer_care_contact",
        "description": "Consumer care details (phone/email)",
        "required": True,
        "check_type": "regex",
        "pattern": r"(\d{10}|[\w\.-]+@[\w\.-]+\.\w+)",
        "legal_reference": "Schedule 4, Rule 6"
    },
    "LMPC-06-ORIGIN": {
        "field": "country_of_origin",
        "description": "Country of origin (for imported goods)",
        "required": False,
        "check_type": "presence",
        "legal_reference": "Schedule 4, Rule 6"
    },
    "LMPC-09-LEGIBILITY": {
        "field": "legibility",
        "description": "Declarations must be legible",
        "required": True,
        "check_type": "readability",
        "legal_reference": "Rule 9"
    }
}

# ===== VERDICT CONSTANTS =====
VERDICT_COMPLIANT = "COMPLIANT"
VERDICT_NON_COMPLIANT = "NON-COMPLIANT"
VERDICT_NEEDS_REVIEW = "NEEDS REVIEW"

# ===== CONFIDENCE LEVELS =====
HIGH_CONFIDENCE = 0.75  # Lowered from 0.85 for better detection
MEDIUM_CONFIDENCE = 0.50  # Lowered from 0.65 for better detection
LOW_CONFIDENCE = 0.3   # Lowered from 0.50 for fallback

# ===== DEMO MODE =====
ENABLE_DEMO_MODE = True
DEMO_IMAGES = ["demo_rice_compliant.png", "demo_cereal_noncompliant.png", "demo_oil_needsreview.png"]

# ===== UI SETTINGS =====
PAGE_TITLE = "ComplyScan: Legal Metrology Compliance Assistant"
PAGE_ICON = "📦"
LAYOUT = "wide"

# ===== LEGAL DISCLAIMER =====
LEGAL_DISCLAIMER = """
**Disclaimer:** ComplyScan is an AI-assisted screening tool providing indicative compliance assessment only. 
It is not a substitute for official legal determination. Final compliance decisions must be made by authorized 
Legal Metrology Officers. The rule mapping is indicative and must be verified against the current notified 
provisions of the Legal Metrology (Packaged Commodities) Rules, 2011 before enforcement action.

This prototype screens ordinary retail pre-packaged commodities and explicitly excludes medical devices.
"""
