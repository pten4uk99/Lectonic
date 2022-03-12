import os

from PIL import Image
from django.core.files.storage import default_storage

from speakers.settings import BASE_DIR


class TestUploadingImages:
    MEDIA_URL = '/test_media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media')

    filename = 'test_image_QWERTYUIOP.jpg'

    path = os.path.join(MEDIA_ROOT, filename)

    def __create_folder(self):
        if not os.path.exists(self.MEDIA_ROOT):
            os.mkdir(self.MEDIA_ROOT)

    def create_image(self):
        self.__create_folder()

        image = Image.new('RGB', (640, 480))

        if not default_storage.exists(self.filename):
            image.save(self.path)

        return default_storage.open(self.filename)


test_image = TestUploadingImages()
