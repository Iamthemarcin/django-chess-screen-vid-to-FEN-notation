from django.db import models


class MyImg(models.Model):
    Img = models.ImageField(upload_to='images/')


class MyVid(models.Model):
    Vid = models.FileField(upload_to='videos/')




