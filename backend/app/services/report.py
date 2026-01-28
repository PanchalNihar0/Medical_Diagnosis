"""
PDF Report Generation Service.

Generates professional PDF reports for prediction results that users
can download and share with their healthcare providers.
"""
from io import BytesIO
from datetime import datetime
from typing import Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

from app.api.schemas.common import PredictionResult, ConfidenceLevel
from app.config import logger


class ReportGenerator:
    """Generates PDF reports for medical predictions."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Create custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1e40af')
        ))
        
        self.styles.add(ParagraphStyle(
            name='ReportSubtitle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            alignment=TA_CENTER,
            textColor=colors.gray
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=15,
            spaceAfter=10,
            textColor=colors.HexColor('#1e40af')
        ))
        
        self.styles.add(ParagraphStyle(
            name='ReportBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            alignment=TA_JUSTIFY
        ))
        
        self.styles.add(ParagraphStyle(
            name='Disclaimer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.gray,
            alignment=TA_CENTER,
            spaceBefore=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='Warning',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#dc2626'),
            spaceBefore=5
        ))
    
    def generate_report(
        self,
        prediction: PredictionResult,
        patient_inputs: dict,
        include_recommendations: bool = True,
        include_explanations: bool = True
    ) -> bytes:
        """
        Generate a PDF report for a prediction result.
        
        Args:
            prediction: The prediction result
            patient_inputs: Dictionary of input values
            include_recommendations: Whether to include lifestyle tips
            include_explanations: Whether to include SHAP explanations
            
        Returns:
            PDF file as bytes
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        # Header
        story.append(Paragraph("Health Risk Assessment Report", self.styles['ReportTitle']))
        story.append(Paragraph(
            f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self.styles['ReportSubtitle']
        ))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1e40af')))
        story.append(Spacer(1, 20))
        
        # Risk Assessment Result
        story.append(Paragraph("Risk Assessment Result", self.styles['SectionHeader']))
        
        result_color = self._get_result_color(prediction.prediction, prediction.confidence_level)
        result_text = "Elevated Risk Detected" if prediction.prediction == 1 else "Low Risk Indicated"
        
        result_data = [
            ["Condition Assessed:", prediction.disease.replace("_", " ").title()],
            ["Risk Level:", result_text],
            ["Confidence:", f"{prediction.confidence_level.value} ({prediction.probability:.1%})"],
        ]
        
        result_table = Table(result_data, colWidths=[2.5*inch, 4*inch])
        result_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('TEXTCOLOR', (1, 1), (1, 1), result_color),
        ]))
        story.append(result_table)
        story.append(Spacer(1, 15))
        
        # Recommendation
        story.append(Paragraph("Recommendation", self.styles['SectionHeader']))
        story.append(Paragraph(prediction.recommendation, self.styles['ReportBody']))
        story.append(Spacer(1, 10))
        
        # Input Summary
        story.append(Paragraph("Input Data Summary", self.styles['SectionHeader']))
        
        input_data = [[k.replace("_", " ").title(), str(v)] for k, v in patient_inputs.items()]
        
        # Split into two columns if many inputs
        if len(input_data) > 8:
            mid = len(input_data) // 2
            left_data = input_data[:mid]
            right_data = input_data[mid:]
            
            # Pad shorter list
            while len(left_data) < len(right_data):
                left_data.append(["", ""])
            while len(right_data) < len(left_data):
                right_data.append(["", ""])
            
            combined = [[l[0], l[1], r[0], r[1]] for l, r in zip(left_data, right_data)]
            input_table = Table(combined, colWidths=[1.8*inch, 1.4*inch, 1.8*inch, 1.4*inch])
        else:
            input_table = Table(input_data, colWidths=[3*inch, 3.5*inch])
        
        input_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        story.append(input_table)
        story.append(Spacer(1, 15))
        
        # Contributing Factors (SHAP)
        if include_explanations and prediction.top_factors:
            story.append(Paragraph("Key Contributing Factors", self.styles['SectionHeader']))
            
            for factor in prediction.top_factors[:5]:
                direction = "↑" if factor.contribution > 0 else "↓"
                impact = "increases" if factor.contribution > 0 else "decreases"
                story.append(Paragraph(
                    f"• <b>{factor.display_name}</b>: {factor.value:.2f} — {impact} risk",
                    self.styles['ReportBody']
                ))
            story.append(Spacer(1, 10))
        
        # Lifestyle Recommendations
        if include_recommendations and prediction.lifestyle_tips:
            story.append(Paragraph("Lifestyle Recommendations", self.styles['SectionHeader']))
            
            for tip in prediction.lifestyle_tips:
                story.append(Paragraph(f"• {tip}", self.styles['ReportBody']))
            story.append(Spacer(1, 10))
        
        # Disclaimer
        story.append(HRFlowable(width="100%", thickness=1, color=colors.gray))
        story.append(Paragraph(
            "<b>IMPORTANT DISCLAIMER</b>",
            self.styles['Disclaimer']
        ))
        story.append(Paragraph(
            prediction.disclaimer,
            self.styles['Disclaimer']
        ))
        story.append(Paragraph(
            "This report is generated by an AI-powered screening tool and is intended "
            "for informational purposes only. It should not replace professional medical "
            "advice, diagnosis, or treatment. Always consult with a qualified healthcare "
            "provider regarding any medical conditions or concerns.",
            self.styles['Disclaimer']
        ))
        
        # Build PDF
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        logger.info(f"Generated PDF report for {prediction.disease} ({len(pdf_bytes)} bytes)")
        
        return pdf_bytes
    
    def _get_result_color(self, prediction: int, confidence: ConfidenceLevel) -> colors.Color:
        """Get appropriate color for result based on prediction and confidence."""
        if prediction == 0:
            return colors.HexColor('#059669')  # Green for low risk
        elif confidence == ConfidenceLevel.HIGH:
            return colors.HexColor('#dc2626')  # Red for high confidence high risk
        else:
            return colors.HexColor('#d97706')  # Amber for moderate confidence high risk


# Singleton instance
_report_generator = None


def get_report_generator() -> ReportGenerator:
    """Get the singleton report generator instance."""
    global _report_generator
    if _report_generator is None:
        _report_generator = ReportGenerator()
    return _report_generator
