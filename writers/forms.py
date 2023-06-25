
from django import forms

from birdie.models import  Order

class UploadForm(forms.Form):

    upload_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))