# tasks/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category = self.request.query_params.get('category')
        due_date = self.request.query_params.get('due_date')  # Obtener el parámetro de fecha de vencimiento
        priority = self.request.query_params.get('priority')  # Obtener el parámetro de prioridad

        # Filtrar las tareas por usuario
        queryset = Task.objects.filter(user=self.request.user)

        if category:
            queryset = queryset.filter(category_id=category)
        
        if due_date:  # Filtrar por fecha de vencimiento
            queryset = queryset.filter(due_date=due_date)
        
        if priority:  # Filtrar por prioridad
            queryset = queryset.filter(priority=priority)

        return queryset

    def get_object(self):
        """Override to ensure the task belongs to the authenticated user."""
        obj = super().get_object()
        if obj.user != self.request.user:
            raise NotFound("Task not found.")
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """Ensure the user is the owner of the task before deletion."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Aquí puedes personalizar la creación de la categoría si es necesario
        serializer.save()

