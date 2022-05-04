import os.path
import time

from django.core import management
from django.http import FileResponse
from django.shortcuts import render, redirect

from speakers.settings import DEFAULT_HOST


DIR = 'log/'
DUMP_PATH = DIR + 'dbdump.json'


def index(request):
    context = {'files': []}

    for file in os.listdir('log'):

        if file.startswith('__init__'):
            continue

        name = file.split('.')[0]
        context['files'].append({
            'path': DIR + file,
            'filename': file,
            'name': name
        })

    if os.path.exists(DUMP_PATH):
        context['last_change'] = time.ctime(os.path.getmtime(DUMP_PATH))

    return render(request, 'adminapp/index.html', context)


def save_file(request):
    for file in os.listdir('log'):
        name = request.GET.get('file')

        if name == file.split('.')[0]:
            return FileResponse(open(DIR + file, 'rb'))

    return redirect('admin_index')


def make_dump(request):
    management.call_command('dumpdatautf8', '--indent=2', '-o', DUMP_PATH)
    return redirect('admin_index')
