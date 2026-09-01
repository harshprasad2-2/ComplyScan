# ComplyScan Demo Walkthrough (5 Minutes)

**For SIH Judges - Follow this exact sequence to see ComplyScan in action.**

---

## Pre-Demo Setup (Do this before judges arrive)

```powershell
# Terminal 1: Start the app
cd f:\Dev\SIH\ComplyScan
.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

The browser should open to `http://localhost:8501`

If not, manually open browser and navigate there.

---

## Demo Script (5 Minutes)

### Segment 1: Problem Statement (1 min)

**You say:**
> "Team Nexus is solving SIH26034: Compliance checking of packaged commodities under Legal Metrology rules.
> 
> The problem is: India has millions of packaged products. Manual inspection is slow, subjective, and inconsistent.
> ComplyScan automates this using AI to screen labels in seconds, generate audit trails, and help both inspectors and manufacturers."

**What judges see:** App homepage

---

### Segment 2: Load Demo A (Compliant) (1.5 min)

1. Go to **New Scan** tab (should already be there)

2. In sidebar, select **"Demo A: Compliant Rice Package"** from dropdown

3. Make sure **"Load Demo Images"** checkbox is checked

4. Click the Upload area or wait for demo to process

**System shows:**
- Original image
- Preprocessed image
- Extracted declarations table:
  - Manufacturer: Sunrise Foods ✓
  - Net Quantity: 5 kg ✓
  - MRP: ₹620 ✓
  - Date: 08/2026 ✓
  - Consumer Care: 1800-123-4567 ✓
  
5. Scroll down to see:
   - **Verdict:** COMPLIANT ✅ (green)
   - **Compliance Score:** ~90%+
   - **Overall Confidence:** ~85%+

6. Expand each rule in "Rule-by-Rule Evaluation":
   - Show 1-2 rules (PASS status)
   - Say: *"Each rule maps to a specific Legal Metrology requirement"*

**You say:**
> "This is a compliant package. All mandatory declarations are present and properly formatted. 
> The system extracted text via OCR, parsed the fields using regex and keyword matching, 
> then checked each against compliance rules. No violations found."

---

### Segment 3: Generate Report (1 min)

7. Click **"📄 Generate PDF Report"** button

8. Wait ~5 seconds for report to generate

9. Click **"📥 Download PDF Report"** button

10. Open the PDF in a new tab (if your system allows)

**PDF should show:**
- Report title: "COMPLIANCE SCREENING REPORT"
- Overall verdict: COMPLIANT
- Rules summary table
- Disclaimer

**You say:**
> "ComplyScan generates professional PDF reports that inspectors can file immediately. 
> This eliminates paperwork and creates a searchable audit trail."

---

### Segment 4: Load Demo B (Non-Compliant) (1.5 min)

11. Back to Streamlit, click **"↺ Scan Another"** button

12. This time, select **"Demo B: Missing Consumer Care"** from dropdown

13. Let it process

**System shows:**
- Same images and extraction
- **BUT** in extracted fields table: No "Consumer Care Contact" row (or empty value)

14. Scroll to **Violations Found**:
   - Red box: **"consumer_care_contact: Required field missing..."**

15. **Verdict:** NON-COMPLIANT ❌ (red)

**You say:**
> "This package is missing required consumer care information. The system flagged this as NON-COMPLIANT.
> In a real scenario, an enforcement officer would write a notice. Our system generates that evidence automatically."

---

### Segment 5: Dashboard (Optional, 30 sec)

16. Click **"Dashboard"** in sidebar

**Shows:**
- KPI cards: Total Scans, Compliant, Non-Compliant, Needs Review
- Pie chart of compliance distribution

**You say:**
> "Inspectors can track compliance trends across regions and product categories using the dashboard.
> This gives enforcement agencies data they've never had before."

---

### Segment 6: Technical Explanation (Judge Q&A) (Optional)

If judge asks "How does this work?", explain:

**Image Processing:**
> "We use OpenCV to preprocess images: deskew, denoise, enhance contrast. This makes OCR much more accurate."

**OCR:**
> "RapidOCR extracts text locally, offline. We chose it over cloud APIs for speed, privacy, and cost at national scale."

**Extraction:**
> "We use regex patterns for structured formats (prices, dates, quantities) and keyword anchors for free-text fields (manufacturer address near 'Mfd by' phrase)."

**Rules:**
> "Every rule is a config record mapping to a specific Legal Metrology provision. If a rule changes, we update JSON, not code."

**Confidence:**
> "When OCR confidence is low, we mark the scan as 'NEEDS REVIEW' instead of guessing. The judge/officer makes the final call."

---

## Judge's Likely Questions & Answers

| Question | Answer |
|----------|--------|
| **Why not use an LLM?** | For legally-consequential decisions, deterministic rules are safer and auditable. LLMs are probabilistic. |
| **How accurate is this?** | Depends on image quality. We don't quote a single % because it varies by field and image. Confidence scoring routes uncertain cases to human review. |
| **Can this replace inspectors?** | No. It's decision support. Inspectors make final calls. This just saves them hours of manual work. |
| **What about other languages?** | MVP supports English + basic Hindi. Full multilingual support is Phase 2 (after SIH). |
| **Why not just use Google Cloud Vision?** | Cost at national scale, data sovereignty, offline capability. RapidOCR is open-source and self-hosted. |
| **How do you handle curved bottles?** | Preprocessing handles tilted/curved packages reasonably well. Extreme cases get routed to "NEEDS REVIEW". |
| **What's your MVP timeline?** | Built in 24 hours for hackathon. Phase 2 (post-SIH): mobile app, YOLO panel detection, full RBAC, government deployment path. |

---

## Demo Troubleshooting

**If app won't start:**
```bash
# Check Python is installed
python --version  # Should show 3.11+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Try again
python -m streamlit run app.py
```

**If demo images don't load:**
```bash
# Generate them manually
python -c "from modules.demo_data import generate_all_demo_images; generate_all_demo_images()"
```

**If OCR gives no results:**
- This is OK for demo. Say: "This is why we include demo images - RapidOCR installation is platform-dependent."
- Fall back to manually explaining extraction logic.

**If PDF doesn't download:**
- Check file permissions in `/reports/` folder
- Download may be blocked by browser - show the file exists in Explorer instead

---

## Key Points to Hammer

✅ **Problem:** Manual inspection is slow, inconsistent, not auditable
✅ **Solution:** Automated screening with transparent rule engine
✅ **For inspectors:** Instant reports, searchable history, dashboard trends
✅ **For manufacturers:** Self-check before printing/listing
✅ **MVP approach:** Explainable, local, offline-ready
✅ **Safety:** Routes uncertain cases to humans, never auto-decides when unsure

---

## After Demo

- **Offer to take questions** for 2-3 minutes
- **Show code** if judge asks (modules/ are well-commented)
- **Mention roadmap:** Mobile, YOLO, PostgreSQL backend, production deployment
- **End with:** "This is a proof-of-concept showing the vision. In production, we'd add mobile, multilingual, and scale to thousands of daily inspections."

---

**Total Demo Time: 5 minutes (including pauses)**
**Total Q&A Time: 3-5 minutes**
**Total: 8-10 minutes**

Good luck! 🎯
