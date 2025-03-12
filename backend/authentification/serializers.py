from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(use_url=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'nombre', 'apellido', 'direccion', 'profile_picture']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': True},
            'nombre': {'required': True},
            'apellido': {'required': True},
            'direccion': {'required': True},
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            nombre=validated_data['nombre'],
            apellido=validated_data['apellido'],
            direccion=validated_data['direccion'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # Actualiza los campos del usuario
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.apellido = validated_data.get('apellido', instance.apellido)
        instance.direccion = validated_data.get('direccion', instance.direccion)

        # Manejar la actualización de la contraseña
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        # Manejar la actualización de la imagen de perfil
        profile_picture = validated_data.get('profile_picture')
        if profile_picture:
            instance.profile_picture = profile_picture

        instance.save()
        return instance
