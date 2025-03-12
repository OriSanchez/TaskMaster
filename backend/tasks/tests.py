# tasks/tests.py
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Task, Category

User = get_user_model()

class TaskTests(APITestCase):
    def setUp(self):
        # Crear un usuario de prueba y autenticarlo
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Crear una categoría de prueba y asignarla a self.category
        self.category = Category.objects.create(name="Work")

        # Definir la URL de la lista de tareas
        self.task_url = reverse("task-list")

    def test_create_task(self):
        data = {
            "title": "Test Task",
            "description": "This is a test task",
            "due_date": "2024-12-31",
            "priority": "M",
            "status": "P",
            "category": self.category.id
        }
        response = self.client.post(self.task_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_task(self):
        # Crear una tarea para recuperar
        task = Task.objects.create(
            title="Retrieve Task",
            description="Task to retrieve",
            due_date="2024-12-31",
            priority="M",
            status="P",
            category=self.category,
            user=self.user
        )
        response = self.client.get(reverse("task-detail", args=[task.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Retrieve Task")
    
    def test_update_task(self):
        # Crear una tarea para actualizar
        task = Task.objects.create(
            title="Old Task",
            description="Old description",
            due_date="2024-12-31",
            priority="L",
            status="P",
            category=self.category,
            user=self.user
        )
        data = {
            "title": "Updated Task",
            "description": "Updated description",
            "due_date": "2025-01-01",
            "priority": "H",
            "status": "IP",
            "category": self.category.id
        }
        response = self.client.put(reverse("task-detail", args=[task.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, "Updated Task")
        self.assertEqual(task.priority, "H")
        self.assertEqual(task.status, "IP")

    def test_delete_task(self):
        # Crear una tarea para eliminar
        task = Task.objects.create(
            title="Delete Task",
            description="Task to delete",
            due_date="2024-12-31",
            priority="L",
            status="P",
            category=self.category,
            user=self.user
        )
        response = self.client.delete(reverse("task-detail", args=[task.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_filter_tasks_by_category(self):
        Task.objects.create(
            title="Work Task", description="Task 1", due_date="2024-12-31", priority="M", 
            status="P", category=self.category, user=self.user
        )
        response = self.client.get(self.task_url, {"category": self.category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_tasks_by_priority(self):
        Task.objects.create(
            title="High Priority Task", description="High priority", due_date="2024-12-31", 
            priority="H", status="P", category=self.category, user=self.user
        )
        response = self.client.get(self.task_url, {"priority": "H"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_owner_can_view_task(self):
        # Crear una tarea para otro usuario
        other_user = User.objects.create_user(username="otheruser", password="testpass")
        task = Task.objects.create(
            title="Other's Task",
            description="Should not be accessible",
            due_date="2024-12-31",
            priority="M",
            status="P",
            category=self.category,
            user=other_user
        )
        response = self.client.get(reverse("task-detail", args=[task.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

