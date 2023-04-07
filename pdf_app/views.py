import subprocess
from django.shortcuts import render
from django.http import FileResponse
from .forms import InsuranceClaimForm

class InsuranceClaimFormView:
    def get(self, request):
        form = InsuranceClaimForm()
        context = {'form': form}
        return render(request, 'index.html', context)

    def post(self, request):
        form = InsuranceClaimForm(request.POST)
        if form.is_valid():
            # Get the form data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            dob = form.cleaned_data['dob']
            current_date = form.cleaned_data['current_date']
            member_id = form.cleaned_data['member_id']
            claim_number = form.cleaned_data['claim_number']

            # Run the Python script to generate the PDF file
            command = ['python', 'generate_pdf.py', first_name, last_name, dob, current_date, member_id, claim_number]
            subprocess.run(command)

            # Return the generated PDF file as a response
            with open('insurance_claim.pdf', 'rb') as pdf_file:
                response = FileResponse(pdf_file)
                return response
    
        context = {'form': form}
        return render(request, 'index.html', context)

