import os

from PIL import Image
from rest_framework import serializers

EMAIL_VALIDATOR = r'^[A-Za-z0-9-]+@[A-Za-z0-9-]+\.[a-z]{2,4}$'


class PhotoValidator:
    ALLOWED_FORMATS = ['jpg', 'jpeg', 'png', 'JPG', 'JPEG']
    default_msg = 'Фотография может быть только в формате "jpg" или "png"'

    def __init__(self, path):
        self.path = path
        self.photo = Image.open(path)
        self.name = path.split('\\')[-1]
        self.format = self.name.split('.')[-1]

    def __is_valid(self, msg=None):
        if self.format not in self.ALLOWED_FORMATS:
            raise serializers.ValidationError(msg or self.default_msg)
        return True

    def __resize(self):
        new_img = self.photo
        if self.photo.width > 1080 and self.photo.height > 1080:
            diff = self.photo.width / self.photo.height
            new_img = self.photo.resize((int(1080 * diff), 1080))
        return new_img

    def save(self, msg=None):
        self.__is_valid(msg)

        new_img = self.__resize()
        new_img.save(self.path)

        return self.path
