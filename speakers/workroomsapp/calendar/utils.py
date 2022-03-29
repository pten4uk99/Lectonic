def build_photo_path(request, part_of_path):
    host = request.build_absolute_uri('/')

    if host[-1] == '/' and part_of_path[0] == '/':
        new_path = part_of_path.replace('/', '', 1)
        return host + new_path

    elif host[-1] != '/' and part_of_path[0] != '/':
        return host + '/' + part_of_path

    return host + part_of_path
