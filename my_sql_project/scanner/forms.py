from django import forms

class ScanForm(forms.Form):
    url = forms.URLField(label='Target URL', widget=forms.URLInput(attrs={'class': 'form-control'}))