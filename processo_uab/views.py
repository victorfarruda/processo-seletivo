from django.http import request
from django.shortcuts import render

def inicio_page(request):
    return render(request, 'index.html', {})