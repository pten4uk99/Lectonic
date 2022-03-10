import os

from PIL import Image
from django.core.files.storage import default_storage

from speakers.settings import MEDIA_ROOT


class TestUploadingImages:
    folder = 'test'
    filename = 'test_image_QWERTYUIOP.jpg'

    path = os.path.join(folder, filename)
    full_path = os.path.join(MEDIA_ROOT, path)

    def __create_folder(self):
        folder_path = os.path.join(MEDIA_ROOT, self.folder)

        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

    def start(self):
        self.__create_folder()

        image = Image.new('RGB', (640, 480))

        if not default_storage.exists(self.path):
            image.save(self.full_path)
        return default_storage.open(self.path)

    def stop(self):
        default_storage.delete(self.filename)


test_image = TestUploadingImages()
