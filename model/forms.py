from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(required=False)
    file = forms.FileField()