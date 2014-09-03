from django import forms


class DivertForm(forms.Form):
    flight_path = forms.CharField(widget=forms.Textarea(attrs={
        'cols': 75, 'rows': 30}), max_length=1000)