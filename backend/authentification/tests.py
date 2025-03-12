from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from PIL import Image
import io
from django.core.files.uploadedfile import SimpleUploadedFile

class UserTests(APITestCase):

    def create_image_file(self):
        # Crea una imagen azul
        image = Image.new('RGB', (100, 100), color='blue')
        img_io = io.BytesIO()
        image.save(img_io, 'JPEG')
        img_io.name = 'test_image.jpg'  # Nombre de archivo
        img_io.seek(0)  # Reiniciar el puntero al principio
        return img_io

    def setUp(self):
        # Define las variables username y password aquí
        self.username = 'taskm'
        self.password = 'Camioneta2024.*'
        self.user = User.objects.create_user(
            username=self.username,
            email='taskm288@gmail.com',
            password=self.password,
            nombre='Test',
            apellido='User',
            direccion='123 Test St',
            estado='Test State',
            profile_picture=None
        )
        
        # Inicializa el token de acceso
        self.token = RefreshToken.for_user(self.user)

    def test_register_user(self):
        url = reverse('authentification:register')
        image_file = self.create_image_file()  # Genera la imagen
        data = {
            'username': 'nadamasprobar',  # Asegúrate de que este nombre de usuario sea único
            'email': 'taskm386@gmail.com',
            'nombre': 'Test Name',
            'apellido': 'Test Surname',
            'direccion': '123 Test St',
            'password': 'testpassword',
            'profile_picture': SimpleUploadedFile(image_file.name, image_file.getvalue(), content_type='image/jpeg'),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))
        url = reverse('authentification:user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_user_edit(self):
        self.client.login(username=self.username, password=self.password)

        # Crear archivo de imagen simulado para subida
        profile_picture = SimpleUploadedFile(
            "test_image.jpg", self.create_image_file().getvalue(), content_type="image/jpeg"
        )

        # Datos de usuario
        data = {
            'username': self.username,
            'nombre': 'Updated Name',
            'apellido': 'Updated Surname',
            'direccion': '789 Updated St',
            'password': 'newpassword',
            'profile_picture': profile_picture
        }

        # Envío de solicitud PUT usando formato 'multipart'
        response = self.client.put(
            reverse('authentification:user-edit'),
            data,
            format='multipart'
        )

        # Para depuración detallada, ver respuesta JSON
        print("Response JSON:", response.json())

        # Verificación del código de respuesta esperado
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset(self):
        url = reverse('authentification:password_reset')
        data = {
            'email': self.user.email,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))
        url = reverse('authentification:delete_account')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username=self.user.username).exists())  # Verifica que el usuario fue eliminado

