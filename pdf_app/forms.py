from django import forms

class InsuranceClaimForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    dob = forms.DateField()
    current_date = forms.DateField()
    member_id = forms.CharField(max_length=100)
    claim_number = forms.CharField(max_length=100)
