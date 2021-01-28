from django import forms
from .models import Image, Size


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        id = Image.id
        fields = ('img_url', 'image')


class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ('width', 'height')
