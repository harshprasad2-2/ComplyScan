"""
ComplyScan - Main Streamlit Application
AI-assisted Legal Metrology compliance screening system.
"""

import streamlit as st
import cv2
import numpy as np
from pathlib import Path
from datetime import datetime

# Import modules
from modules.config import (
    APP_NAME, APP_VERSION, APP_SUBTITLE, LEGAL_DISCLAIMER,
    UPLOADS_FOLDER, DEMO_IMAGES_FOLDER
)
from modules.database import get_db
from modules.image_processing import preprocess_image, draw_evidence_boxes, save_processed_image
from modules.ocr_engine import extract_text_from_image
from modules.extraction import extract_declarations
from modules.rules_engine import evaluate_compliance
from modules.report_generator import generate_compliance_report
from modules.demo_data import generate_all_demo_images
from modules.utils import generate_scan_id, get_readable_timestamp, format_confidence

# Page configuration
st.set_page_config(
    page_title="ComplyScan",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
st.sidebar.title("ComplyScan")
st.sidebar.write(f"v{APP_VERSION}")

page = st.sidebar.radio("Navigation", 
    ["New Scan", "History", "Dashboard", "About", "Help"])

# ===== NEW SCAN PAGE =====
if page == "New Scan":
    st.title("📦 ComplyScan")
    st.subheader("AI-assisted packaged commodity compliance screening")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("### Upload Package Label Image")
        st.write("Upload a photograph of a package label for compliance screening.")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=["jpg", "jpeg", "png", "bmp"],
            key="image_upload"
        )
        
        # Or load demo
        st.write("---")
        st.write("### Or Load a Demo")
        demo_option = st.selectbox("Select demo package:", [
            "None",
            "Demo A: Compliant Rice Package",
            "Demo B: Missing Consumer Care",
            "Demo C: MRP Tax Issue"
        ])
    
    with col2:
        st.write("### Settings")
        mode = st.radio("Mode:", ["Simple", "Technical"])
        enable_demo = st.checkbox("Load Demo Images", value=True)
    
    # Process image
    if uploaded_file or demo_option != "None":
        st.write("---")
        st.write("### Processing...")
        
        # Determine image source
        image_file = None
        demo_mode = False
        
        if demo_option != "None" and enable_demo:
            # Map demo option to file
            demo_files = {
                "Demo A: Compliant Rice Package": "demo_a_compliant.png",
                "Demo B: Missing Consumer Care": "demo_b_missing_care.png",
                "Demo C: MRP Tax Issue": "demo_c_mrp_issue.png"
            }
            demo_path = DEMO_IMAGES_FOLDER / demo_files[demo_option]
            
            # Generate demo images if they don't exist
            if not demo_path.exists():
                generate_all_demo_images()
            
            image_file = str(demo_path)
            demo_mode = True
        elif uploaded_file:
            # Save uploaded file
            uploaded_path = UPLOADS_FOLDER / uploaded_file.name
            uploaded_path.parent.mkdir(parents=True, exist_ok=True)
            with open(uploaded_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            image_file = str(uploaded_path)
        
        if image_file:
            try:
                # Load and preprocess image
                image = cv2.imread(image_file)
                if image is None:
                    st.error("Could not load image")
                else:
                    # Preprocess
                    processed, enhanced, gray = preprocess_image(image)
                    
                    # Extract text using OCR (use enhanced grayscale, not binary)
                    ocr_results = extract_text_from_image(enhanced)
                    
                    if not ocr_results:
                        st.warning("⚠️ No text could be detected in the image. Image may be too unclear.")
                    
                    # Extract declarations
                    extracted_fields = extract_declarations(ocr_results)
                    
                    # Evaluate compliance
                    evaluation = evaluate_compliance(extracted_fields)
                    
                    # Display results
                    st.write("---")
                    st.write("### Results")
                    
                    # Verdict display
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        verdict = evaluation['verdict']
                        if verdict == "COMPLIANT":
                            st.success(f"✅ {verdict}")
                        elif verdict == "NON-COMPLIANT":
                            st.error(f"❌ {verdict}")
                        else:
                            st.warning(f"⚠️ {verdict}")
                    
                    with col2:
                        st.metric("Compliance Score", f"{evaluation['compliance_score']:.1f}%")
                    
                    with col3:
                        st.metric("Overall Confidence", f"{evaluation['overall_confidence']:.1%}")
                    
                    # Display images
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Original Image**")
                        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        st.image(image_rgb, use_container_width=True)
                    
                    with col2:
                        st.write("**Preprocessed (Enhanced)**")
                        enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB)
                        st.image(enhanced_rgb, use_container_width=True)
                    
                    # Extracted fields
                    st.write("---")
                    st.write("### Extracted Declarations")
                    
                    fields_display = []
                    for field_name, field_data in extracted_fields.items():
                        if field_data.get('value') is not None:
                            fields_display.append({
                                'Field': field_name.replace('_', ' ').title(),
                                'Value': field_data['value'],
                                'Confidence': format_confidence(field_data.get('confidence', 0)),
                                'Method': field_data.get('extraction_method', 'N/A')
                            })
                    
                    if fields_display:
                        st.table(fields_display)
                    else:
                        st.info("No declarations could be extracted from the image.")
                    
                    # Rule evaluation
                    st.write("---")
                    st.write("### Rule-by-Rule Evaluation")
                    
                    for rule in evaluation['rule_results']:
                        status_icon = "✅" if rule['status'] == 'PASS' else ("❌" if rule['status'] == 'FAIL' else "⚠️")
                        with st.expander(f"{status_icon} {rule['field'].replace('_', ' ').title()}"):
                            st.write(f"**Status:** {rule['status']}")
                            st.write(f"**Description:** {rule['description']}")
                            st.write(f"**Legal Reference:** {rule['legal_reference']}")
                            st.write(f"**Explanation:** {rule['explanation']}")
                            if rule['detected_value']:
                                st.write(f"**Detected Value:** {rule['detected_value']}")
                                st.write(f"**Confidence:** {format_confidence(rule['confidence'])}")
                    
                    # Violations
                    if evaluation['violations']:
                        st.write("---")
                        st.write("### Violations Found")
                        for violation in evaluation['violations']:
                            st.error(f"**{violation['field'].title()}**: {violation['explanation']}")
                            st.write(f"Legal Reference: {violation['legal_reference']}")
                    
                    # Save and generate report
                    st.write("---")
                    st.write("### Actions")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("📄 Generate PDF Report"):
                            scan_id = generate_scan_id()
                            scan_data = {
                                'scan_id': scan_id,
                                'timestamp': get_readable_timestamp(),
                                'product_name': demo_option if demo_mode else uploaded_file.name,
                                **evaluation
                            }
                            
                            # Generate report
                            report_path = generate_compliance_report(scan_data, image_file)
                            
                            # Save to database
                            db = get_db()
                            db.save_scan({
                                'scan_id': scan_id,
                                'timestamp': get_readable_timestamp(),
                                'filename': demo_option if demo_mode else uploaded_file.name,
                                'product_name': demo_option if demo_mode else uploaded_file.name,
                                'verdict': evaluation['verdict'],
                                'confidence_score': evaluation['overall_confidence'],
                                'image_path': image_file,
                                'report_path': report_path,
                                'extracted_fields': extracted_fields,
                                'violations': evaluation['violations']
                            })
                            
                            # Provide download
                            with open(report_path, 'rb') as f:
                                st.download_button(
                                    label="📥 Download PDF Report",
                                    data=f.read(),
                                    file_name=Path(report_path).name,
                                    mime="application/pdf"
                                )
                            
                            st.success(f"✅ Scan saved (ID: {scan_id})")
                    
                    with col2:
                        if st.button("↺ Scan Another"):
                            st.rerun()
                    
                    # Disclaimer
                    st.write("---")
                    st.info(LEGAL_DISCLAIMER)
            
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
                st.write("Please try with a different image or check the image format.")

# ===== HISTORY PAGE =====
elif page == "History":
    st.title("📋 Scan History")
    
    db = get_db()
    scans = db.get_scan_history(limit=50)
    
    if scans:
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            verdict_filter = st.selectbox("Filter by Verdict:", ["All", "COMPLIANT", "NON-COMPLIANT", "NEEDS REVIEW"])
        
        with col2:
            st.write("&nbsp;")
        
        with col3:
            if st.button("🗑️ Clear History"):
                db.clear_all_scans()
                st.rerun()
        
        # Display scans
        for scan in scans:
            if verdict_filter != "All" and scan['verdict'] != verdict_filter:
                continue
            
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.write(f"**{scan['product_name']}**")
                st.write(f"Scanned: {scan['timestamp']}")
            
            with col2:
                if scan['verdict'] == "COMPLIANT":
                    st.success(scan['verdict'])
                elif scan['verdict'] == "NON-COMPLIANT":
                    st.error(scan['verdict'])
                else:
                    st.warning(scan['verdict'])
            
            with col3:
                st.write(f"{scan['confidence_score']:.1%}")
            
            with col4:
                if st.button("View", key=scan['scan_id']):
                    # TODO: Show detailed view
                    st.write("Detailed view - to be implemented")
            
            st.divider()
    else:
        st.info("No scans in history yet. Start with a new scan!")

# ===== DASHBOARD PAGE =====
elif page == "Dashboard":
    st.title("📊 Dashboard")
    
    db = get_db()
    stats = db.get_dashboard_stats()
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Scans", stats['total_scans'])
    
    with col2:
        st.metric("Compliant", stats['compliant'])
    
    with col3:
        st.metric("Non-Compliant", stats['non_compliant'])
    
    with col4:
        st.metric("Needs Review", stats['needs_review'])
    
    # Stats
    st.write("---")
    
    if stats['total_scans'] > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Compliance distribution
            import plotly.graph_objects as go
            
            fig = go.Figure(data=[go.Pie(
                labels=['Compliant', 'Non-Compliant', 'Needs Review'],
                values=[stats['compliant'], stats['non_compliant'], stats['needs_review']],
                marker=dict(colors=['#27ae60', '#e74c3c', '#f39c12'])
            )])
            fig.update_layout(title="Compliance Distribution", height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("### Statistics")
            if stats['total_scans'] > 0:
                compliance_rate = (stats['compliant'] / stats['total_scans']) * 100
                st.write(f"**Compliance Rate:** {compliance_rate:.1f}%")
            
            st.write(f"**Average per Category:**")
            st.write(f"- Compliant: {stats['compliant']/stats['total_scans']*100:.1f}%")
            st.write(f"- Non-Compliant: {stats['non_compliant']/stats['total_scans']*100:.1f}%")
            st.write(f"- Needs Review: {stats['needs_review']/stats['total_scans']*100:.1f}%")
    else:
        st.info("No scan data available yet.")

# ===== ABOUT PAGE =====
elif page == "About":
    st.title("About ComplyScan")
    
    st.write("""
    ### ComplyScan v1.0.0
    
    **AI-assisted Legal Metrology Compliance Screening System**
    
    ComplyScan is an innovative solution developed by Team Nexus for SIH 2026 to automate 
    compliance checking of packaged commodities under the Legal Metrology (Packaged Commodities) Rules, 2011.
    
    #### Key Features
    - 📷 Image upload and automated analysis
    - 🔍 OCR-based text extraction
    - ✅ Rule-based compliance checking
    - 📄 PDF report generation
    - 📊 Compliance dashboard and history
    - 🎯 Explainable decision-making
    
    #### Technology Stack
    - **Frontend:** Streamlit
    - **Image Processing:** OpenCV
    - **OCR:** RapidOCR
    - **Rules Engine:** Python (regex + keyword matching)
    - **Database:** SQLite
    - **Reporting:** ReportLab
    
    #### Legal Scope
    This is a screening aid for ordinary retail pre-packaged commodities. Final compliance 
    determination must be made by authorized Legal Metrology Officers.
    
    #### Mandatory Declarations Checked
    ✓ Manufacturer/Packer/Importer name and address
    ✓ Commodity name
    ✓ Net quantity
    ✓ Manufacture/packing date
    ✓ Maximum Retail Price (MRP)
    ✓ MRP inclusive of taxes declaration
    ✓ Consumer care contact
    ✓ Country of origin (for imported goods)
    
    ---
    """)
    
    st.info(LEGAL_DISCLAIMER)

# ===== HELP PAGE =====
elif page == "Help":
    st.title("❓ Help & FAQ")
    
    st.write("""
    ### How to Use ComplyScan
    
    1. **Upload Image:** Go to "New Scan" and upload a photo of the package label
    2. **View Results:** ComplyScan will analyze the image and display results
    3. **Review Details:** Check extracted fields and rule evaluation
    4. **Generate Report:** Create a PDF report for record-keeping
    5. **Track History:** View all scans in "History" page
    
    ### FAQ
    
    **Q: What types of images can I upload?**
    A: JPG, PNG, BMP, and TIFF images. Clear, well-lit photos work best.
    
    **Q: How accurate is the compliance check?**
    A: Accuracy depends on image quality and OCR capabilities. When in doubt, 
    the system marks the scan as "Needs Review" for manual verification.
    
    **Q: Can this replace human inspectors?**
    A: No. ComplyScan is a decision-support tool. Final determinations must be made 
    by authorized Legal Metrology Officers.
    
    **Q: What should I do if text isn't being detected?**
    A: Try a clearer, better-lit photo. Avoid reflective surfaces and extreme angles.
    
    **Q: How long are reports stored?**
    A: Reports are stored locally on this machine. Export them for long-term archival.
    
    ### Contact
    For support, visit the SIH portal or contact Team Nexus.
    """)

# Footer
st.write("---")
st.write(f"ComplyScan v{APP_VERSION} • Team Nexus • SIH 2026")
