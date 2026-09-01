"""
ComplyScan Report Generator Module
Creates PDF compliance reports using ReportLab.
"""

import json
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib import colors
from modules.config import REPORTS_FOLDER, LEGAL_DISCLAIMER

class ReportGenerator:
    """Generates PDF compliance reports."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()
    
    def _add_custom_styles(self):
        """Add custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=6,
            alignment=1  # Center
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
            spaceBefore=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='VerdictCompliant',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#27ae60'),
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='VerdictNonCompliant',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#e74c3c'),
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='VerdictNeedsReview',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#f39c12'),
            fontName='Helvetica-Bold'
        ))
    
    def generate_report(self, scan_data: dict, image_path: str = None) -> str:
        """
        Generate a PDF compliance report.
        
        Args:
            scan_data (dict): Complete scan results from rules_engine
            image_path (str): Path to original scanned image
        
        Returns:
            str: Path to generated PDF file
        """
        # Create report file path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"compliance_report_{timestamp}.pdf"
        report_path = REPORTS_FOLDER / report_filename
        
        # Create PDF document
        doc = SimpleDocTemplate(
            str(report_path),
            pagesize=letter,
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch,
            leftMargin=0.75 * inch,
            rightMargin=0.75 * inch
        )
        
        # Build document content
        elements = []
        
        # Header
        elements.append(Paragraph("COMPLYSCAN", self.styles['CustomTitle']))
        elements.append(Paragraph("Compliance Screening Report", self.styles['Heading2']))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Report metadata
        metadata = [
            ['Report Generated:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ['Report ID:', scan_data.get('scan_id', 'N/A')],
            ['Product:', scan_data.get('product_name', 'Unknown')],
        ]
        metadata_table = Table(metadata, colWidths=[2 * inch, 4 * inch])
        metadata_table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(metadata_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Verdict section
        elements.append(Paragraph("Overall Verdict", self.styles['CustomHeading']))
        
        verdict = scan_data.get('verdict', 'UNKNOWN')
        verdict_style = f'Verdict{verdict.replace("-", "")}'
        if verdict_style not in self.styles:
            verdict_style = 'VerdictNeedsReview'
        
        elements.append(Paragraph(f"<b>{verdict}</b>", self.styles[verdict_style]))
        elements.append(Paragraph(
            f"Compliance Score: <b>{scan_data.get('compliance_score', 0):.1f}%</b>",
            self.styles['Normal']
        ))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Rules summary
        elements.append(Paragraph("Rules Evaluation Summary", self.styles['CustomHeading']))
        
        summary_data = [
            ['Total Rules Checked', str(scan_data.get('total_rules_checked', 0))],
            ['Rules Passed', str(scan_data.get('rules_passed', 0))],
            ['Rules Failed', str(scan_data.get('rules_failed', 0))],
            ['Requires Review', str(scan_data.get('rules_review', 0))],
        ]
        summary_table = Table(summary_data, colWidths=[2.5 * inch, 3.5 * inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Violations section
        if scan_data.get('violations'):
            elements.append(Paragraph("Identified Violations", self.styles['CustomHeading']))
            
            violations_data = [['Rule', 'Field', 'Issue', 'Reference']]
            for violation in scan_data['violations']:
                violations_data.append([
                    violation.get('rule_id', 'N/A'),
                    violation.get('field', 'N/A'),
                    violation.get('explanation', 'N/A')[:50] + '...',
                    violation.get('legal_reference', 'N/A')
                ])
            
            violations_table = Table(violations_data, colWidths=[1 * inch, 1.2 * inch, 2.3 * inch, 1.5 * inch])
            violations_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
                ('FONT', (0, 1), (-1, -1), 'Helvetica', 8),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('PADDING', (0, 0), (-1, -1), 4),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))
            elements.append(violations_table)
            elements.append(Spacer(1, 0.3 * inch))
        
        # Disclaimer
        elements.append(PageBreak())
        elements.append(Paragraph("Legal Disclaimer", self.styles['CustomHeading']))
        elements.append(Paragraph(LEGAL_DISCLAIMER, self.styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        
        return str(report_path)


def generate_compliance_report(scan_data: dict, image_path: str = None) -> str:
    """Convenience function to generate a report."""
    generator = ReportGenerator()
    return generator.generate_report(scan_data, image_path)
