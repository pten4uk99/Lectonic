from django.core.files.storage import default_storage


def get_id_with_prefix(self_id):
    id_with_prefix = '101' + str(self_id).rjust(4, '0')
    return id_with_prefix


def document_image(instance, filename):
    name = get_id_with_prefix(instance.person.user.pk)
    path = f'{name}/documents/{name}_{filename}'

    if default_storage.exists(path):
        default_storage.delete(path)

    return path
