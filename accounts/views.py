from django.shortcuts import render, redirect
from django.db.models import Q
from .models import User

def register(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            error ="This email is already registered."
        else:
            User.objects.create(username=username, email=email, password=password)
            return redirect('login')
        

    return render(request, 'accounts/register.html', {'error': error})

def login_view(request):
    mensagem = None
    error = None

    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')

        try:
            user = User.objects.get(
                Q(email=login) | Q(username=login),
                password=password)
            request.session['user_id'] = user.id_user
            return redirect('dashboard')  # <- muda aqui
        except User.DoesNotExist:
            error = 'Email ou password errados'

    return render(request, 'accounts/login.html', {'error': error})
