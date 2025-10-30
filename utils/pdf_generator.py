# utils/pdf_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_plan_pdf(plan_data, output_path="holiday_plan.pdf"):
    """
    Create a simple, elegant PDF summary of the generated travel plan.
    """
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []

    title = f"Holiday Plan for {plan_data.get('destination', 'Unknown')}"
    elements.append(Paragraph(title, styles['Title']))
    elements.append(Spacer(1, 12))

    # Weather
    weather = plan_data.get("weather", {})
    elements.append(Paragraph("<b>Weather Summary</b>", styles["Heading2"]))
    elements.append(Paragraph(f"Description: {weather.get('description', '-')}", styles["Normal"]))
    elements.append(Paragraph(f"Temperature: {weather.get('temp', '-')} °C", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Budget
    budget = plan_data.get("budget", {})
    elements.append(Paragraph("<b>Budget Overview</b>", styles["Heading2"]))
    elements.append(Paragraph(f"Estimate: ${budget.get('estimate', '-')}", styles["Normal"]))
    flag_status = "Within limit" if not budget.get("flagged", False) else "Exceeded limit"
    elements.append(Paragraph(f"Status: {flag_status}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Activities
    elements.append(Paragraph("<b>Top Activities</b>", styles["Heading2"]))
    for act in plan_data.get("activities", []):
        elements.append(Paragraph(f"• {act}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Itinerary
    elements.append(Paragraph("<b>Itinerary</b>", styles["Heading2"]))
    itinerary = plan_data.get("itinerary", {})
    data = [["Day", "Plan"]]
    for day, desc in itinerary.items():
        data.append([day, desc])

    table = Table(data, colWidths=[80, 380])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Notes
    notes = plan_data.get("notes", "")
    if notes:
        elements.append(Paragraph("<b>Notes</b>", styles["Heading2"]))
        elements.append(Paragraph(notes, styles["Normal"]))

    doc.build(elements)

    return os.path.abspath(output_path)
