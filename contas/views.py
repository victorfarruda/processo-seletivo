from django.contrib.auth import authenticate, login
from django.http import request
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import LoginForm


def login_page(request):
    login_form = LoginForm(request.POST or None)
    if request.user.is_authenticated():
        return redirect('inicio')
    if request.method == 'POST':
        if login_form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(request.POST)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
    context = {
        'login': login_form,
    }
    return render(request, 'contas/login.html', context)

