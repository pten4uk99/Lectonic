import os.path
import time

from django.core import management
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from speakers.settings import DEFAULT_HOST


def index(request):
    context = {}

    if os.path.exists('db/dbdump.json'):
        context['last_change'] = time.ctime(os.path.getmtime('db/dbdump.json'))
        context['dbdump'] = DEFAULT_HOST + '/dbdump.json'

    return render(request, 'adminapp/index.html', context)


def save_dump(request):
    return FileResponse(open('db/dbdump.json', 'rb'))


def make_dump(request):
    management.call_command('dumpdatautf8', '--indent=2', '-o', 'db/dbdump.json')
    return redirect('admin_index')
