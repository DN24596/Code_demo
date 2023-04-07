from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

# Define data for the form fields
first_name = "John"
last_name = "Doe"
dob = "01/01/1970"
current_date = "03/23/2023"
member_id = "123456"
claim_number = "789012"

# Define a function to create a paragraph with a specified style and text
def create_paragraph(text, style):
    return Paragraph(text, style)

# Define the styles for the form fields
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
styles.add(ParagraphStyle(name='Signature', alignment=TA_CENTER, fontSize=12))

# Define the content for the PDF form
content = []

# Add a spacer to separate the fields
content.append(Spacer(1, 0.25 * inch))

# Add the first and last name fields
content.append(create_paragraph("First Name:", styles['Normal']))
content.append(create_paragraph(first_name, styles['Normal']))
content.append(create_paragraph("Last Name:", styles['Normal']))
content.append(create_paragraph(last_name, styles['Normal']))

# Add a spacer to separate the fields
content.append(Spacer(1, 0.25 * inch))

# Add the date of birth and current date fields
content.append(create_paragraph("Date of Birth:", styles['Normal']))
content.append(create_paragraph(dob, styles['Normal']))
content.append(create_paragraph("Current Date:", styles['Normal']))
content.append(create_paragraph(current_date, styles['Normal']))

# Add a spacer to separate the fields
content.append(Spacer(1, 0.25 * inch))

# Add the member ID and claim number fields
content.append(create_paragraph("Member ID:", styles['Normal']))
content.append(create_paragraph(member_id, styles['Normal']))
content.append(create_paragraph("Claim Number:", styles['Normal']))
content.append(create_paragraph(claim_number, styles['Normal']))

# Add a spacer to separate the fields
content.append(Spacer(1, 0.5 * inch))

# Add a signature field
content.append(create_paragraph("Signature:", styles['Normal']))
content.append(create_paragraph("______________________________", styles['Signature']))

# Define the filename for the generated PDF file
filename = "insurance_claim.pdf"

# Generate the PDF form
doc = SimpleDocTemplate(filename, pagesize=letter)
doc.build(content)
