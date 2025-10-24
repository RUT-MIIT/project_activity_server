from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from showcase.models import ProjectApplication, ApplicationStatus
from accounts.models import User, Role


class ProjectApplicationAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.status = ApplicationStatus.objects.create(
            code="created", name="Создана", position=1, is_active=True
        )
        self.role = Role.objects.create(code="test", name="Тестовая роль")
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Имя",
            last_name="Фамилия",
            role=self.role,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_project_application(self):
        url = reverse("project-application-list")
        data = {
            "title": "Тестовая заявка",
            "description": "Описание",
            "company": "Компания",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ProjectApplication.objects.count(), 1)
        app = ProjectApplication.objects.first()
        self.assertEqual(app.title, data["title"])
        self.assertEqual(app.status, self.status)
        self.assertEqual(app.author, self.user)

    def test_update_project_application(self):
        app = ProjectApplication.objects.create(
            title="Старая заявка",
            description="Описание",
            company="Компания",
            status=self.status,
            author=self.user,
        )
        url = reverse("project-application-detail", args=[app.id])
        data = {"title": "Новая заявка"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        app.refresh_from_db()
        self.assertEqual(app.title, "Новая заявка")

    def test_delete_project_application(self):
        app = ProjectApplication.objects.create(
            title="Удаляемая заявка",
            description="Описание",
            company="Компания",
            status=self.status,
            author=self.user,
        )
        url = reverse("project-application-detail", args=[app.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(ProjectApplication.objects.filter(id=app.id).exists())
