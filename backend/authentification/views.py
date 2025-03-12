# authentification/views.py
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib import messages
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.http import JsonResponse




User = get_user_model()

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = []

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomPasswordResetView(APIView):
    permission_classes = [AllowAny]
    email_template_name = 'authentification/password_reset_email.html'
    template_name = 'authentification/password_reset.html'
    success_url = reverse_lazy('authentification:password_reset_done')

    # No se requiere autenticación para esta vista
    permission_classes = []  # Asegúrate de que esta lista esté vacía

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')  # Obtener el correo del JSON

        if not email:
            return Response({'error': 'El campo de correo electrónico es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(email=email)  # Buscar el usuario por el correo electrónico

        if not users.exists():
            return Response({'error': 'No se encontró un usuario con ese correo electrónico.'}, status=status.HTTP_400_BAD_REQUEST)

        # Si hay múltiples usuarios, puedes manejarlo de varias maneras:
        if users.count() > 1:
            return Response({'error': 'Se encontraron múltiples usuarios con ese correo electrónico. Por favor, contacte al soporte.'}, status=status.HTTP_400_BAD_REQUEST)

        user = users.first()  # Obtener el primer usuario (siempre que solo haya un único usuario)

        # Generar el uid y el token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url = request.build_absolute_uri(reverse('authentification:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

        # Enviar el correo
        send_mail(
            subject='Recuperación de contraseña',
            message=f'Para restablecer su contraseña, haga clic en el siguiente enlace: {url}',
            from_email='noreply@example.com',  # Cambia por tu dirección de correo
            recipient_list=[user.email],
        )

        return Response({'message': 'Se ha enviado un enlace de recuperación de contraseña a su correo electrónico.'}, status=status.HTTP_200_OK)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'authentification/password_reset_confirm.html'
    success_url = reverse_lazy('authentification:password_reset_complete')

    def form_valid(self, form):
        form.save()  # Restablecer la contraseña
        messages.success(self.request, "¡Su contraseña ha sido restablecida con éxito!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ha ocurrido un error al restablecer la contraseña.")
        return super().form_invalid(form)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        user = request.user
        # Aquí puedes devolver la información del perfil del usuario
        return Response({
            'username': user.username,
            'nombre': user.nombre,
            'email': user.email,
            'apellido': user.apellido,
            'direccion': user.direccion,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,  # Agrega la URL de la foto de perfil
        })


class UserEditView(APIView):
    def put(self, request):
        user = request.user
        print(request.data)
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user  # Obtener el usuario autenticado

        # Eliminar el usuario
        user.delete()

        return Response({'message': 'Usuario eliminado con éxito.'}, status=status.HTTP_204_NO_CONTENT)