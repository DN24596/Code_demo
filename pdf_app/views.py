from django.http import HttpResponse

def generate_claim(request):
    # Get the necessary data from the request
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    dob = request.POST.get('dob')
    member_id = request.POST.get('member_id')
    claim_num = request.POST.get('claim_num')

    # Generate the PDF file
    generate_pdf(first_name, last_name, dob, member_id, claim_num)

    # Return the generated PDF file as a response
    with open("output.pdf", "rb") as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="claim.pdf"'
        return response
