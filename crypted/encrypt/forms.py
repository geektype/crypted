from django import forms


class EncryptForm(forms.Form):
    data = forms.CharField(label="data", max_length=256)
    public_key = forms.FileField()
