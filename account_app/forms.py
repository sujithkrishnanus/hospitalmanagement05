from django import forms
from .models import Prescription, Bill

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medicine', 'dosage', 'instructions']

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['item_name', 'total_price']