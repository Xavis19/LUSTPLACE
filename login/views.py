from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')
            return redirect('lista_productos')
        else:
            messages.error(request, 'Credenciales inválidas')
    
    return render(request, 'Login/login.html')

def registro_view(request):  # ✅ RENOMBRAR
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validaciones
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'Login/registro.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return render(request, 'Login/registro.html')
        
        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        
        # Login automático
        auth_login(request, user)
        messages.success(request, '¡Usuario creado exitosamente!')
        return redirect('lista_productos')
    
    return render(request, 'Login/registro.html')