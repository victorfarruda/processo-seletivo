from django.http import request
from django.shortcuts import render

def inicio(request):
    return render(request, 'base.html', {})