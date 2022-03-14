from django.core.files.storage import default_storage


def get_id_with_prefix(self_id):
    id_with_prefix = '101' + str(self_id).rjust(4, '0')
    return id_with_prefix


def person_image(instance, filename):
    user_id = get_id_with_prefix(instance.user.pk)
    path = f'{user_id}/photo/{user_id}_{filename}'

    if default_storage.exists(path):
        default_storage.delete(path)

    return path


def document_image(instance, filename):
    user_id = get_id_with_prefix(instance.person.user.pk)
    path = f'{user_id}/documents/{user_id}_{filename}'

    if default_storage.exists(path):
        default_storage.delete(path)

    return path


def diploma_image(instance, filename):
    user_id = get_id_with_prefix(instance.lecturer.person.user.pk)
    path = f'{user_id}/diploma/{user_id}_{filename}'

    if default_storage.exists(path):
        default_storage.delete(path)

    return path


def lecturer_lecture_image(instance, filename):
    lecture_id = get_id_with_prefix(instance.lecture_request.lecture.pk)

    user_id = get_id_with_prefix(instance.lecturer.person.user.pk)
    path = f'{user_id}/lectures/lecturer/{lecture_id}_{filename}'

    if user_id is None:
        raise AttributeError('Ошибка при построении пути к фотографии: '
                             'ни один из связанных объектов не существует')

    if path and default_storage.exists(path):
        default_storage.delete(path)

    return path
