from django.core.files.storage import default_storage


class ImagePath:
    __slots__ = ('__document_image', '__diploma_image')

    def __init__(self, document_image=False, diploma_image=False):
        self.__document_image = document_image
        self.__diploma_image = diploma_image

    @staticmethod
    def get_id_with_prefix(self_id):
        id_with_prefix = '101' + str(self_id).rjust(4, '0')
        return id_with_prefix

    def __call__(self, *args, **kwargs):
        instance, filename = args

        path = None

        if self.__document_image:
            name = self.get_id_with_prefix(instance.person.user.pk)
            path = f'{name}/documents/{name}_{filename}'
        elif self.__diploma_image:
            name = self.get_id_with_prefix(instance.lecturer.person.user.pk)
            path = f'{name}/diploma/{name}_{filename}'

        if path and default_storage.exists(path):
            default_storage.delete(path)

        return path


document_image = ImagePath(document_image=True)
diploma_image = ImagePath(diploma_image=True)
