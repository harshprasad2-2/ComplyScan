# ComplyScan

**AI-assisted Legal Metrology Compliance Screening System**

ComplyScan is an innovative hackathon prototype developed by Team Nexus for the Smart India Hackathon 2026 (Problem Statement SIH26034). It automates compliance checking of packaged commodities against the Legal Metrology (Packaged Commodities) Rules, 2011.

---

## 📋 Quick Links

- **🎯 Live Demo:** http://localhost:8501 (after running locally)
- **📖 Full Documentation:** See [README.md](README.md)
- **🚀 Deployment Guide:** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **🎬 Demo Walkthrough:** See [RUN_DEMO.md](RUN_DEMO.md)
- **✅ Build Status:** See [BUILD_COMPLETE.md](BUILD_COMPLETE.md)

---

## Quick Start

### Installation

**Prerequisites:**
- Python 3.11 or higher
- Windows/Mac/Linux

**Step 1: Clone or download this repository**

```bash
cd ComplyScan
```

**Step 2: Create virtual environment**

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
source .venv/bin/activate   # Mac/Linux
```

**Step 3: Install dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Step 4: Run the application**

```bash
python -m streamlit run app.py
```

The app will open at `http://localhost:8501`

## Features

### ✅ Core Functionality
- 📷 **Image Upload:** Support for JPG, PNG, BMP, TIFF
- 🔍 **OCR Text Extraction:** Uses RapidOCR for local, offline text recognition
- ✅ **Automated Rule Checking:** Verifies compliance against Legal Metrology rules
- 📄 **PDF Report Generation:** Creates detailed compliance reports
- 📊 **Dashboard:** View compliance statistics and trends
- 💾 **SQLite History:** Local database for scan records
- 🎯 **Explainability:** Every decision is explained step-by-step

### 🎨 User Interface
- **New Scan:** Upload images and view instant compliance verdicts
- **History:** Browse all previous scans with filters
- **Dashboard:** View compliance statistics and trends
- **Demo Mode:** Test with pre-built synthetic package images
- **Technical Mode:** Detailed explanations for Q&A

## Compliance Rules

The system checks for these mandatory declarations (Legal Metrology Rules 2011):

✓ **Manufacturer/Packer/Importer** - Name and address
✓ **Commodity Name** - Common or generic name
✓ **Net Quantity** - Weight/volume/number in standard units
✓ **Manufacture/Pack Date** - MM/YYYY format
✓ **Maximum Retail Price (MRP)** - Price value
✓ **MRP Inclusive Tax Declaration** - "Inclusive of all taxes" phrase
✓ **Consumer Care Contact** - Phone or email
✓ **Country of Origin** - For imported goods

## Verdicts

The system returns one of three verdicts:

- **COMPLIANT ✅** - All required declarations present and properly formatted
- **NON-COMPLIANT ❌** - One or more mandatory declarations missing or incorrect
- **NEEDS REVIEW ⚠️** - Image quality too low or text detection uncertain (requires human review)

## Architecture

### Pipeline Stages

```
Image Upload
    ↓
[1] Image Preprocessing (OpenCV)
    - Deskew, denoise, enhance contrast
    ↓
[2] OCR Extraction (RapidOCR)
    - Extract text + confidence + bounding boxes
    ↓
[3] Field Parsing (Regex + Keywords)
    - Manufacturer, quantity, MRP, date, etc.
    ↓
[4] Rule Validation (Config-driven)
    - Check each field against compliance rules
    ↓
Verdict (COMPLIANT / NON-COMPLIANT / NEEDS REVIEW)
    ↓
Report Generation (PDF)
    ↓
Database Storage (SQLite)
```

### Module Structure

```
modules/
├── config.py           # Configuration and rule definitions
├── database.py         # SQLite database handlers
├── image_processing.py # OpenCV image preprocessing
├── ocr_engine.py       # RapidOCR integration
├── extraction.py       # Field extraction using regex + keywords
├── rules_engine.py     # Compliance rule evaluation
├── report_generator.py # PDF report creation
├── demo_data.py        # Synthetic demo images
└── utils.py            # Helper functions
```

## Demo Mode

The application includes **3 synthetic demo packages** for testing:

1. **Demo A:** Compliant rice package (all declarations present, correct format)
2. **Demo B:** Missing consumer care contact (will fail)
3. **Demo C:** MRP without "inclusive of tax" wording (will fail)

Load these from the "Load Demo" dropdown without uploading files.

## Usage Examples

### Example 1: Uploading a Real Package Image

1. Navigate to **New Scan** tab
2. Upload JPG/PNG of a package label
3. System automatically:
   - Extracts text using OCR
   - Parses declarations
   - Checks compliance rules
   - Generates verdict
4. View extracted fields and rule results
5. Generate PDF report
6. Access history anytime

### Example 2: Using Demo Mode

1. Select "Demo A: Compliant Rice Package" from dropdown
2. System processes demo image
3. Shows expected result: **COMPLIANT ✅**
4. Verify each field was extracted correctly
5. Generate and download sample PDF report

### Example 3: Checking Compliance History

1. Go to **History** tab
2. View all previous scans with verdicts
3. Filter by "Compliant" / "Non-Compliant" / "Needs Review"
4. Click any scan to view details

## Technical Details

### Why This Architecture?

**Q: Why not just use OCR?**
A: Raw OCR gives unstructured text. Our pipeline adds:
- Image preprocessing for accuracy
- Pattern matching for reliable field extraction
- Rule engine for legally-grounded verdicts
- Confidence scoring to route uncertain cases to human review

**Q: Why RapidOCR instead of cloud APIs?**
A: 
- Works offline (no internet required)
- No per-call costs
- Data stays local (privacy)
- Faster response
- Supports Indian languages

**Q: Why SQLite instead of PostgreSQL?**
A:
- Single file database (portable)
- No server installation needed
- Works on any machine
- Good for MVP prototyping

**Q: Why config-driven rules?**
A:
- Rules can be updated without code changes
- Legal Metrology experts can modify thresholds
- Easy to audit and maintain
- Transparent rule mapping

## Key Design Decisions

1. **Confidence-aware:** Never auto-decide when uncertain - routes to "Needs Review"
2. **Explainable:** Every verdict includes "why" explanation
3. **Evidence-based:** Shows which parts of the image produced which fields
4. **Conservative:** Flags edge cases rather than guessing
5. **Local-first:** Offline-capable, no external APIs required

## Known Limitations

- Font size cannot be verified without physical scale (e.g., ruler) in photo
- Very curved/reflective packaging may not process well
- Requires reasonable image quality (not blurred/too dark)
- Multilingual support limited (focus on English + basic Hindi)
- Panel detection done via preprocessing (not ML-based panel localization)

These are MVP trade-offs. Production version would add:
- YOLO-based panel detection
- Calibration-based font measurement
- Full multilingual OCR
- Mobile app with reference markers

## Testing

Run unit tests:

```bash
pytest tests/ -v
```

Test extraction logic:

```bash
pytest tests/test_extraction.py
```

Test rules engine:

```bash
pytest tests/test_rules.py
```

## File Structure

```
ComplyScan/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── RUN_DEMO.md            # Step-by-step demo instructions
├── run.bat                # Windows batch launcher
│
├── modules/
│   ├── __init__.py
│   ├── config.py          # App configuration & rules
│   ├── database.py        # SQLite database
│   ├── image_processing.py# OpenCV preprocessing
│   ├── ocr_engine.py      # RapidOCR wrapper
│   ├── extraction.py      # Field extraction
│   ├── rules_engine.py    # Rule evaluation
│   ├── report_generator.py# PDF generation
│   ├── demo_data.py       # Demo image creation
│   └── utils.py           # Helper functions
│
├── tests/
│   ├── __init__.py
│   ├── test_extraction.py # Extraction tests
│   └── test_rules.py      # Rules engine tests
│
├── data/
│   └── complyscan.db      # SQLite database (auto-created)
│
├── uploads/               # User-uploaded images
├── reports/               # Generated PDF reports
├── assets/
│   └── demo_images/       # Synthetic demo images
│
└── .venv/                 # Virtual environment (git-ignored)
```

## FAQ

**Q: Does this replace inspectors?**
A: No. It's a decision-support tool. Authorized Legal Metrology Officers must make final determinations.

**Q: What about medical devices or other categories?**
A: This MVP explicitly excludes medical devices and focuses on ordinary retail packaged commodities.

**Q: Can judges modify rules?**
A: Yes, in production. Rules are in `modules/config.py` as structured data, not hardcoded logic.

**Q: How do I transfer this to another laptop?**
A: Copy the `ComplyScan` folder (except `.venv`). On new machine, recreate venv and reinstall dependencies.

**Q: What's the accuracy rate?**
A: We don't quote a single number. Accuracy depends on image quality and varies by field. Low-confidence reads are marked "NEEDS REVIEW" rather than auto-decided.

**Q: Can I use this in production?**
A: This is an MVP. Production would add security, RBAC, cloud deployment, and extensive testing. See roadmap in architecture docs.

## Legal Disclaimer

**ComplyScan is an AI-assisted screening tool providing indicative compliance assessment only.**

This is NOT a substitute for official legal determination. Final compliance decisions must be made by authorized Legal Metrology Officers under the Legal Metrology (Packaged Commodities) Rules, 2011.

The rule mapping presented in this prototype is indicative and must be verified against the current notified version of the regulations before any enforcement action is taken.

This prototype:
- Screens ordinary retail pre-packaged commodities
- Explicitly excludes medical devices
- Does not claim exhaustive coverage of all provisions
- Requires manual verification for edge cases

---

**Team Nexus | SIH 2026 | Problem SIH26034**
