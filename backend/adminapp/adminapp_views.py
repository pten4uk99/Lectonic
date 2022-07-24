import os.path

from django.core import management
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from adminapp.services import main_api, MainException
from adminapp.services.auth import auth_api
from adminapp.services.config import DIR, DUMP_PATH


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('data')
        auth_api(email)
    return render(request, 'adminapp/signin.html')


def index(request, code):
    try:
        context = main_api(code)
    except MainException:
        return redirect(reverse('admin_auth'))

    return render(request, 'adminapp/index.html', context)


def save_file(request):
    key = request.GET.get('key')

    for file in os.listdir('log'):
        name = request.GET.get('file')

        if name == file.split('.')[0]:
            return FileResponse(open(DIR + file, 'rb'))

    return redirect('admin_index', code=key)


def make_dump(request):
    key = request.GET.get('key')

    management.call_command('dumpdatautf8', '--indent=2', '-o', DUMP_PATH)
    return redirect('admin_index', code=key)
