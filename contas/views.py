from django.contrib.auth import authenticate, login
from django.http import request
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import LoginForm


def login_page(request):
    if request.user.is_authenticated():
        return redirect('inicio')
    login_form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            print(request.POST)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
    context = {
        'login': login_form,
    }
    return render(request, 'contas/login.html', context)

