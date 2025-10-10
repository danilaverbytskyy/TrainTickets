from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from TrainsProject.settings import LOGOUT_REDIRECT_URL
from client.forms import ClientRegistrationForm, ClientLoginForm, UserUpdateForm, ClientUpdateForm
from client.models import Client


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
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            # Создаем пользователя
            user = form.save()

            # Создаем клиента
            client = Client.objects.create(
                user=user,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                patronymic=form.cleaned_data.get('patronymic'),
                birth_date=form.cleaned_data.get('birth_date'),
                passport=form.cleaned_data.get('passport'),
                phone=form.cleaned_data.get('phone')
            )

            # Обновляем first_name и last_name пользователя
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} был успешно создан! Теперь вы можете войти.')
            return redirect('login')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ClientRegistrationForm()

    return render(request, 'client/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = ClientLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Вы вошли как {username}.")
                return redirect('profile')
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    else:
        form = ClientLoginForm()

    return render(request, 'client/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect(LOGOUT_REDIRECT_URL)


@login_required
def profile_view(request):
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        client = None

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        client_form = ClientUpdateForm(request.POST, instance=client) if client else None

        if user_form.is_valid() and (client_form is None or client_form.is_valid()):
            user_form.save()
            if client_form:
                client_form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        client_form = ClientUpdateForm(instance=client) if client else None

    context = {
        'user_form': user_form,
        'client_form': client_form,
        'client': client
    }

    return render(request, 'client/profile.html', context)
