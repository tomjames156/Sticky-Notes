from django import forms

class ImageUploadForm(forms.Form):
    new_image = forms.FileField(label="",widget=forms.FileInput(attrs={'accept': 'image/*', 'id': 'new_image'}))
