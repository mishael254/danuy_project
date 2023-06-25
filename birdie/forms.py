from django import forms

from .models import  Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['Submissiondate', ' UpdationDate', 'orderNo']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['new_deadline'].widget.attrs['class'] = 'datepicker'


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'remark']


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [ 'file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class FileForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))