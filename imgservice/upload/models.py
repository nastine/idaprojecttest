from django.db import models
from django.core.exceptions import ValidationError, PermissionDenied
from django.core.files import File
import os
import urllib
from urllib.request import urlretrieve
from PIL import Image
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class Image(models.Model):
    id = models.IntegerField(primary_key=True)
    img_url = models.CharField(max_length=1000, blank=True, verbose_name='Ссылка')
    image = models.ImageField(upload_to='images', blank=True, verbose_name='Файл')

    def __str__(self):
        return str(self.id)

    def clean(self):
        if self.img_url and self.image:
            raise ValidationError('Заполните только одно поле')
        if not self.img_url and not self.image:
            raise ValidationError('Заполните хотя бы одно поле')

    def save(self):
        """Store image locally if we have a URL"""
        if not self.image and self.img_url:
            try:
                result = urlretrieve(self.img_url)
                self.image.save(
                        os.path.basename(self.img_url),
                        File(open(result[0], 'rb'))
                        )
            except urllib.error.HTTPError:
                raise ValidationError('Невозможно загрузить изображение по данной ссылке')
        else:
            super(Image, self).save()


class Size(models.Model):
    width = models.IntegerField(blank=True, verbose_name='Высота')
    height = models.IntegerField(blank=True, verbose_name='Ширина')

    def clean(self):
        if not self.width and not self.height:
            raise ValidationError('Для изменения размера изображения заполните хотя бы одно поле')
