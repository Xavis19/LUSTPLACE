from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    UserProfileSerializer
)
from .models import UserProfile

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Usuario creado exitosamente',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_api_view(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login exitoso',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_api_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logout exitoso'})
    except Exception as e:
        return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

# ✅ VISTA PARA VER TODOS LOS USUARIOS (SOLO ADMIN)
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Solo admins pueden ver lista de usuarios
        if self.request.user.profile.is_admin:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_info_view(request):
    """Obtener información del usuario actual"""
    return Response({
        'user': UserSerializer(request.user).data,
        'is_admin': request.user.profile.is_admin if hasattr(request.user, 'profile') else False,
        'permissions': request.user.profile.role.permissions if hasattr(request.user, 'profile') else {}
    })

# =================== VISTAS WEB ===================

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.conf import settings
import os

def web_login_view(request):
    """Vista web para login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo, {user.username}!')
            return redirect('lista_productos')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'authentication/login_modern.html')

def web_register_view(request):
    """Vista web para registro"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validaciones
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
        else:
            # Crear usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            login(request, user)
            messages.success(request, f'¡Registro exitoso! Bienvenido, {user.username}!')
            return redirect('lista_productos')
    
    return render(request, 'authentication/registro_modern.html')

@login_required
def perfil_usuario_view(request):
    """Vista principal del perfil de usuario"""
    profile = request.user.profile
    return render(request, 'authentication/perfil_usuario.html', {
        'profile': profile,
        'user': request.user
    })

@login_required
def editar_perfil_view(request):
    """Vista para editar perfil del usuario"""
    profile = request.user.profile
    
    if request.method == 'POST':
        # Actualizar información básica del usuario
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Actualizar perfil
        profile.phone = request.POST.get('phone', '')
        profile.city = request.POST.get('city', '')
        profile.country = request.POST.get('country', '')
        profile.documento_identidad = request.POST.get('documento_identidad', '')
        profile.tipo_documento = request.POST.get('tipo_documento', '')
        
        # Manejar carga de avatar
        if 'avatar' in request.FILES:
            # Eliminar avatar anterior si existe
            if profile.avatar:
                old_avatar_path = profile.avatar.path
                if os.path.exists(old_avatar_path):
                    os.remove(old_avatar_path)
            
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        messages.success(request, '¡Perfil actualizado exitosamente!')
        return redirect('perfil_usuario')
    
    return render(request, 'authentication/editar_perfil.html', {
        'profile': profile,
        'user': request.user
    })

@login_required
def mis_direcciones_view(request):
    """Vista para gestionar direcciones del usuario"""
    from productos.models import DireccionEnvio
    
    direcciones = DireccionEnvio.objects.filter(user=request.user, activa=True)
    
    return render(request, 'authentication/mis_direcciones.html', {
        'direcciones': direcciones
    })

@login_required
def agregar_direccion_view(request):
    """Vista para agregar nueva dirección"""
    from productos.models import DireccionEnvio
    
    if request.method == 'POST':
        direccion = DireccionEnvio.objects.create(
            user=request.user,
            nombre_completo=request.POST.get('nombre_completo'),
            telefono=request.POST.get('telefono'),
            pais=request.POST.get('pais', 'Ecuador'),
            provincia=request.POST.get('provincia'),
            ciudad=request.POST.get('ciudad'),
            direccion_linea1=request.POST.get('direccion_linea1'),
            direccion_linea2=request.POST.get('direccion_linea2', ''),
            codigo_postal=request.POST.get('codigo_postal'),
            es_principal=request.POST.get('es_principal') == 'on'
        )
        
        # Si es principal, desmarcar otras direcciones principales
        if direccion.es_principal:
            DireccionEnvio.objects.filter(
                user=request.user, 
                es_principal=True
            ).exclude(id=direccion.id).update(es_principal=False)
        
        messages.success(request, '¡Dirección agregada exitosamente!')
        return redirect('mis_direcciones')
    
    return render(request, 'authentication/agregar_direccion.html')

@login_required
def mis_pedidos_view(request):
    """Vista para ver pedidos del usuario"""
    from productos.models import Orden
    
    pedidos = Orden.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    return render(request, 'authentication/mis_pedidos.html', {
        'pedidos': pedidos
    })

@login_required
def mis_favoritos_view(request):
    """Vista para ver productos favoritos"""
    from productos.models import Favorito
    
    favoritos = Favorito.objects.filter(usuario=request.user).order_by('-fecha_agregado')
    
    return render(request, 'authentication/mis_favoritos.html', {
        'favoritos': favoritos
    })

@login_required
def eliminar_direccion_view(request, direccion_id):
    """Vista para eliminar dirección"""
    from productos.models import DireccionEnvio
    
    try:
        direccion = DireccionEnvio.objects.get(id=direccion_id, user=request.user)
        direccion.activa = False
        direccion.save()
        messages.success(request, 'Dirección eliminada exitosamente.')
    except DireccionEnvio.DoesNotExist:
        messages.error(request, 'Dirección no encontrada.')
    
    return redirect('mis_direcciones')

@login_required 
def cambiar_avatar_ajax(request):
    """Vista AJAX para cambiar avatar"""
    if request.method == 'POST' and request.FILES.get('avatar'):
        profile = request.user.profile
        
        # Eliminar avatar anterior
        if profile.avatar:
            old_avatar_path = profile.avatar.path
            if os.path.exists(old_avatar_path):
                os.remove(old_avatar_path)
        
        # Guardar nuevo avatar
        profile.avatar = request.FILES['avatar']
        profile.save()
        
        return JsonResponse({
            'success': True,
            'avatar_url': profile.avatar.url if profile.avatar else None,
            'message': 'Avatar actualizado exitosamente'
        })
    
    return JsonResponse({
        'success': False,
        'message': 'Error al subir la imagen'
    })

def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('lista_productos')

# =================== AUTENTICACIÓN CON GOOGLE ===================

import json
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class GoogleAuthView(View):
    """Vista para manejar autenticación con Google OAuth"""
    
    def post(self, request):
        try:
            # Obtener datos del token de Google
            data = json.loads(request.body)
            google_token = data.get('credential')
            
            if not google_token:
                return JsonResponse({'error': 'No se proporcionó token de Google'}, status=400)
            
            # Verificar token con Google (necesitarás instalar google-auth)
            # Por ahora, simularemos la verificación
            # En producción, debes verificar el token con Google
            
            # Datos de ejemplo (en producción vendrían del token verificado)
            google_user_data = {
                'google_id': data.get('sub', ''),
                'email': data.get('email', ''),
                'first_name': data.get('given_name', ''),
                'last_name': data.get('family_name', ''),
                'picture': data.get('picture', ''),
                'email_verified': data.get('email_verified', True)
            }
            
            # Buscar usuario existente por email o google_id
            user = None
            profile = None
            
            try:
                # Buscar por google_id primero
                profile = UserProfile.objects.get(google_id=google_user_data['google_id'])
                user = profile.user
            except UserProfile.DoesNotExist:
                # Buscar por email
                try:
                    user = User.objects.get(email=google_user_data['email'])
                    profile = user.profile
                    # Vincular cuenta de Google existente
                    profile.google_id = google_user_data['google_id']
                    profile.provider = 'google'
                    profile.google_verified = True
                    profile.save()
                except User.DoesNotExist:
                    # Crear nuevo usuario
                    user = User.objects.create_user(
                        username=google_user_data['email'],
                        email=google_user_data['email'],
                        first_name=google_user_data['first_name'],
                        last_name=google_user_data['last_name']
                    )
                    
                    # Actualizar perfil
                    profile = user.profile
                    profile.google_id = google_user_data['google_id']
                    profile.provider = 'google'
                    profile.google_verified = True
                    profile.email_verificado = google_user_data['email_verified']
                    profile.save()
            
            # Iniciar sesión
            login(request, user)
            
            return JsonResponse({
                'success': True,
                'message': f'¡Bienvenido, {user.first_name or user.username}!',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'google_verified': profile.google_verified
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos JSON inválidos'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

def verificar_google_view(request):
    """Vista para verificar cuenta existente con Google"""
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión primero.')
        return redirect('authentication:web_login')
    
    # Redirigir al flujo de OAuth de Google
    # En producción, usarías la URL de OAuth de Google
    google_oauth_url = "https://accounts.google.com/oauth/authorize"
    client_id = "TU_CLIENT_ID_DE_GOOGLE"  # Configura esto
    redirect_uri = request.build_absolute_uri('/auth/google-callback/')
    scope = "openid email profile"
    
    oauth_url = f"{google_oauth_url}?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type=code"
    
    return redirect(oauth_url)

def google_callback_view(request):
    """Callback de Google OAuth"""
    code = request.GET.get('code')
    
    if not code:
        messages.error(request, 'Error en la verificación de Google.')
        return redirect('authentication:editar_perfil')
    
    # Aquí procesarías el código de Google para obtener el token
    # Por ahora, simulamos una verificación exitosa
    
    if request.user.is_authenticated:
        profile = request.user.profile
        profile.google_verified = True
        profile.email_verificado = True
        profile.save()
        
        messages.success(request, '¡Cuenta verificada exitosamente con Google!')
    
    return redirect('authentication:perfil_usuario')
