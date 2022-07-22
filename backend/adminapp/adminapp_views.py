import os.path
import time
from datetime import datetime, timedelta

from django.conf import settings
from django.core import management
from django.core.mail import send_mail
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from adminapp.models import AuthCode

DIR = 'log/'
DUMP_PATH = DIR + 'dbdump.json'


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('data')

        for admin in settings.ADMINS:
            if admin[0] == 'Nikita':
                if email != admin[1]:
                    return HttpResponse('404')

        AuthCode.objects.all().delete()
        auth_code = AuthCode.objects.create()

        send_mail(
            subject='Код доступа лектоник',
            message=f'{auth_code.key}',
            recipient_list=[email],
            from_email=None
        )
    return render(request, 'adminapp/signin.html')


def index(request, code):
    if not settings.DEBUG:
        auth_code = AuthCode.objects.filter(key=code).first()
        if not auth_code or datetime.now() - timedelta(hours=2) > auth_code.datetime:
            return redirect(reverse('admin_auth'))

    context = {'files': [], 'key_param': code}

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
