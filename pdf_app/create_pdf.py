import io
from datetime import date
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas

def generate_pdf(first_name, last_name, dob, member_id, claim_num):
    # Create a new PDF file
    packet = io.BytesIO()
    can = canvas.Canvas(packet)

    # Set the font size and add the fields
    can.setFontSize(12)
    can.drawString(100, 700, 'First Name: {}'.format(first_name))
    can.drawString(100, 670, 'Last Name: {}'.format(last_name))
    can.drawString(100, 640, 'Date of Birth: {}'.format(dob))
    can.drawString(100, 610, 'Current Date: {}'.format(date.today()))
    can.drawString(100, 580, 'Member ID: {}'.format(member_id))
    can.drawString(100, 550, 'Claim Number: {}'.format(claim_num))

    # Add a signature field
    can.line(100, 500, 250, 500)
    can.drawString(100, 480, 'Signature')

    # Save the PDF file
    can.save()

    # Move to the beginning of the file and create a PdfFileReader object
    packet.seek(0)
    new_pdf = PdfFileReader(packet)

    # Load the existing PDF document
    existing_pdf = PdfFileReader(open('path/to/existing/pdf', 'rb'))

    # Create a PdfFileWriter object for the output PDF
    output = PdfFileWriter()

    # Add the new page to the output PDF
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    # Save the output PDF to a file
    outputStream = open("output.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
