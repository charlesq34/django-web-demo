from django import forms

class URLForm(forms.Form):
    myinput = forms.CharField(label='My URL', max_length=300)


class UploadFileForm(forms.Form):
    file = forms.FileField()
