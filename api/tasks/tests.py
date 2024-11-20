from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Project, Task

class ProjectEndpointTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Créer un projet pour tester
        self.project = Project.objects.create(
            name='Test Project',
            description='Description du projet',
            owner=self.user,
            created_by=self.user
        )

    def test_create_project(self):
        data = {
            'name': 'Nouveau Projet',
            'description': 'Description du nouveau projet'
        }
        response = self.client.post('/api/projects/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Nouveau Projet')

    def test_get_project_list(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_project(self):
        data = {
            'name': 'Projet Mis à Jour',
            'description': 'Description mise à jour'
        }
        response = self.client.put(f'/api/projects/{self.project.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Projet Mis à Jour')

    def test_delete_project(self):
        response = self.client.delete(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class TaskEndpointTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Créer un projet pour lier des tâches
        self.project = Project.objects.create(
            name='Test Project',
            description='Description du projet',
            owner=self.user,
            created_by=self.user
        )

        # Créer une tâche pour tester
        self.task = Task.objects.create(
            title='Test Task',
            project=self.project,
            assigned_to=self.user,
            created_by=self.user,
            start_date='2024-11-20',
            due_date='2024-11-25'
        )

    def test_create_task(self):
        data = {
            'title': 'Nouvelle Tâche',
            'description': 'Description de la tâche',
            'project': self.project.id,
            'start_date': '2024-11-22',
            'due_date': '2024-11-27'
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Nouvelle Tâche')

    def test_get_task_list(self):
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_task(self):
        data = {
            'title': 'Tâche Mise à Jour',
            'status': 'IN_PROGRESS'
        }
        response = self.client.patch(f'/api/tasks/{self.task.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Tâche Mise à Jour')
        self.assertEqual(response.data['status'], 'IN_PROGRESS')

    def test_delete_task(self):
        response = self.client.delete(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
