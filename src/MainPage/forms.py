from django import forms
from .models import MyImg, MyVid


class ImageForm(forms.ModelForm):

    class Meta:
        model = MyImg
        fields = ('Img',)


class VideoForm(forms.ModelForm):

    class Meta:
        model = MyVid
        fields = ('Vid',)

