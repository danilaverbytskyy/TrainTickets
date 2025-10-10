from datetime import datetime
from http.client import HTTPResponse

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from client.models import Client
from .forms import CustomUserCreationForm, ClientRegistrationForm, CustomAuthenticationForm


@staff_member_required
def home(request):
    start_time = datetime.now()
    clients = Client.objects.values('first_name')
    print(f'It took {datetime.now() - start_time}')
    print(clients)
    start_time = datetime.now()
    clients = Client.objects.values_list('first_name', flat=False)
    print(f'It took {datetime.now() - start_time}')
    print(clients)
    start_time = datetime.now()
    clients = Client.objects.all()
    print(f'It took {datetime.now() - start_time}')
    print(clients)

    context = {
        'clients': clients,
        'clients_count': len(clients),
    }
    return render(request, 'client/client.html', context)


@staff_member_required
def show(request, client_id):
    client = Client.objects.get(pk=client_id)

    context = {
        'client': client,
        'full_name': f'{client.last_name} {client.first_name} {client.patronymic}'
    }
    return render(request, 'client/show.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        client_form = ClientRegistrationForm(request.POST)

        if user_form.is_valid() and client_form.is_valid():
            # Создаем пользователя
            user = user_form.save()

            # Создаем клиента и связываем с пользователем
            client = client_form.save(commit=False)
            client.user = user
            client.save()

            # Автоматически входим после регистрации
            login(request, user)
            messages.success(request, f'Добро пожаловать, {client.first_name}! Регистрация прошла успешно!')
            return redirect('home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        user_form = CustomUserCreationForm()
        client_form = ClientRegistrationForm()

    context = {
        'user_form': user_form,
        'client_form': client_form,
        'title': 'Регистрация'
    }
    return render(request, 'client/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.client.first_name}!')
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        else:
            messages.error(request, 'Неверный email или пароль')
    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
        'title': 'Вход в систему'
    }
    return render(request, 'client/login.html', context)


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы')
    return redirect('/')


@login_required
def profile_view(request):
    client = request.user.client  # Получаем связанного клиента
    if not client:
        return HTTPResponse(404)
    context = {
        'user': request.user,
        'client': client
    }
    return render(request, 'client/profile.html', context)