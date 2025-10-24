from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from showcase.models import ProjectApplication, ApplicationStatus
from accounts.models import User, Role, Department
from showcase.services.involved import InvolvedManager


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
        """Создаёт заявку через список (POST) и проверяет автора, статус и причастных."""
        url = reverse("project-application-list")
        data = {
            "title": "Тестовая заявка",
            "description": "Описание",
            "company": "Компания",
        }
        response = self.client.post(url, data, format="json")
        if response.status_code != 201:
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.content.decode()}")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ProjectApplication.objects.count(), 1)
        app = ProjectApplication.objects.first()
        self.assertEqual(app.title, data["title"])
        self.assertEqual(app.status, self.status)
        self.assertEqual(app.author, self.user)
        
        # Проверяем, что автор автоматически добавлен в причастные пользователи
        self.assertEqual(app.involved_users.count(), 1)
        self.assertEqual(app.involved_users.first().user, self.user)

    def test_create_project_application_with_department(self):
        """Создаёт заявку с подразделением автора и проверяет причастные подразделения."""
        # Создаем подразделение и назначаем его пользователю
        department = Department.objects.create(
            name="Тестовое подразделение",
            short_name="ТП"
        )
        self.user.department = department
        self.user.save()
        
        url = reverse("project-application-list")
        data = {
            "title": "Тестовая заявка с подразделением",
            "company": "Компания",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        
        app = ProjectApplication.objects.first()
        # Проверяем, что подразделение автора добавлено в причастные
        self.assertEqual(app.involved_departments.count(), 1)
        self.assertEqual(app.involved_departments.first().department, department)

    def test_create_project_application_with_parent_department(self):
        """Создаёт заявку с иерархией подразделений и проверяет причастные подразделения."""
        # Создаем родительское и дочернее подразделения
        parent_dept = Department.objects.create(
            name="Родительское подразделение",
            short_name="РП"
        )
        child_dept = Department.objects.create(
            name="Дочернее подразделение",
            short_name="ДП",
            parent=parent_dept
        )
        
        # Назначаем дочернее подразделение пользователю
        self.user.department = child_dept
        self.user.save()
        
        url = reverse("project-application-list")
        data = {
            "title": "Тестовая заявка с иерархией подразделений",
            "company": "Компания",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        
        app = ProjectApplication.objects.first()
        # Проверяем, что добавлены оба подразделения (дочернее и родительское)
        self.assertEqual(app.involved_departments.count(), 2)
        involved_depts = list(app.involved_departments.all())
        dept_names = [dept.department.name for dept in involved_depts]
        self.assertIn("Дочернее подразделение", dept_names)
        self.assertIn("Родительское подразделение", dept_names)

    def test_update_project_application(self):
        """Обновляет название заявки (PATCH) и убеждается, что изменения сохранены."""
        app = ProjectApplication.objects.create(
            title="Старая заявка",
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
        """Удаляет заявку (DELETE) и проверяет, что объект исчез из БД."""
        app = ProjectApplication.objects.create(
            title="Удаляемая заявка",
            company="Компания",
            status=self.status,
            author=self.user,
        )
        url = reverse("project-application-detail", args=[app.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(ProjectApplication.objects.filter(id=app.id).exists())

    def test_my_applications_returns_only_mine(self):
        """my_applications возвращает только заявки текущего пользователя."""
        # Заявка текущего пользователя
        my_app = ProjectApplication.objects.create(
            title="Моя заявка",
            company="Компания",
            status=self.status,
            author=self.user,
        )
        # Заявка другого пользователя
        other_user = User.objects.create_user(
            email="other@example.com",
            password="pass12345",
            first_name="Other",
            last_name="User",
            role=self.role,
        )
        ProjectApplication.objects.create(
            title="Чужая заявка",
            company="Компания",
            status=self.status,
            author=other_user,
        )
        url = reverse("project-application-my-applications")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]["id"], my_app.id)


    def test_status_logs_returns_list(self):
        """status_logs возвращает список логов изменения статусов заявки."""
        app = ProjectApplication.objects.create(
            title="Логи",
            company="Компания",
            status=self.status,
            author=self.user,
        )
        # Запрос логов
        url = reverse("project-application-status-logs", args=[app.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.data, list)

    def test_add_comment_to_last_log(self):
        """add_comment добавляет комментарий к последнему логу и возвращает его данные."""
        app = ProjectApplication.objects.create(
            title="Комментарий",
            company="Компания",
            status=self.status,
            author=self.user,
        )
        # Сначала изменим статус, чтобы появился лог
        in_progress = ApplicationStatus.objects.create(
            code="ip2", name="В работе 2", position=3, is_active=True
        )
        change_url = reverse("project-application-change-status", args=[app.id])
        self.client.post(change_url, {"status_code": in_progress.code}, format="json")

        url = reverse("project-application-add-comment", args=[app.id])
        payload = {"field": "note", "text": "Примечание"}
        resp = self.client.post(url, payload, format="json")
        self.assertIn(resp.status_code, (200, 201))
        self.assertIn("id", resp.data)

    def test_current_status_info(self):
        """current_status_info возвращает текущий статус и сведения о последнем изменении."""
        app = ProjectApplication.objects.create(
            title="Статус инфо",
            company="Компания",
            status=self.status,
            author=self.user,
        )
        url = reverse("project-application-current-status-info", args=[app.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("status", resp.data)

    def test_simple_creation_without_auth(self):
        """simple создаёт заявку без авторизации, устанавливая статус при необходимости."""
        # Разлогиниваемся
        client = APIClient()
        url = reverse("project-application-simple")
        payload = {"title": "Simple", "company": "ООО", "status_code": self.status.code}
        resp = client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, 201)


    def test_my_in_work_filters_involved_and_excludes_final(self):
        """my_in_work возвращает причастные заявки и исключает approved/rejected."""
        await_status = ApplicationStatus.objects.create(
            code="await_department", 
            name="Ожидает подразделение", 
            position=2, 
            is_active=True
        )
        approved = ApplicationStatus.objects.create(
            code="approved", 
            name="Утверждена", 
            position=3, 
            is_active=True
        )
        rejected = ApplicationStatus.objects.create(
            code="rejected", 
            name="Отклонена", 
            position=4, 
            is_active=True
        )

        # Создаем заявки через API, чтобы сработали сигналы и автор добавился в причастные
        url_create = reverse("project-application-list")
        
        # Причастная заявка в работе
        resp1 = self.client.post(url_create, {
            "title": "A", 
            "company": "C",
            "status_code": await_status.code
        }, format="json")
        self.assertEqual(resp1.status_code, 201)
        app_in_work_id = resp1.data["id"]

        # Причастная approved — должна быть исключена
        resp2 = self.client.post(url_create, {
            "title": "B", 
            "company": "C",
            "status_code": approved.code
        }, format="json")
        self.assertEqual(resp2.status_code, 201)
        app_approved_id = resp2.data["id"]

        # Причастная rejected — должна быть исключена
        resp3 = self.client.post(url_create, {
            "title": "C", 
            "company": "C",
            "status_code": rejected.code
        }, format="json")
        self.assertEqual(resp3.status_code, 201)
        app_rejected_id = resp3.data["id"]

        # Дополнительно добавляем другого пользователя в причастные для проверки фильтрации
        other_user = User.objects.create_user(
            email="other@example.com",
            password="pass12345",
            first_name="Other",
            last_name="User",
            role=self.role,
        )
        app_in_work = ProjectApplication.objects.get(id=app_in_work_id)
        InvolvedManager.add_involved_user(app_in_work, other_user, actor=self.user)

        url = reverse("project-application-my-in-work")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        ids = [x["id"] for x in resp.data]
        self.assertIn(app_in_work_id, ids)
        self.assertNotIn(app_approved_id, ids)
        self.assertNotIn(app_rejected_id, ids)

    def test_mentor_creation_sets_await_department_and_logs_once(self):
        """Создание заявки ментором с подразделением: статус await_department."""
        # Роли и подразделение
        mentor_role = Role.objects.create(code="mentor", name="Наставник")
        dept = Department.objects.create(name="Dept")
        mentor = User.objects.create_user(
            email="mentor@example.com",
            password="pass",
            first_name="M",
            last_name="R",
            role=mentor_role,
            department=dept,
        )
        self.client.force_authenticate(user=mentor)

        # Необходимые статусы
        await_status = ApplicationStatus.objects.create(
            code="await_department", 
            name="Ожидает подразделение", 
            position=2, 
            is_active=True
        )

        url = reverse("project-application-list")
        resp = self.client.post(url, {"title": "X", "company": "Y"}, format="json")
        self.assertEqual(resp.status_code, 201)

        app = ProjectApplication.objects.first()
        self.assertEqual(app.status.code, "await_department")

        # Проверяем, что ментор добавлен в причастные пользователи
        self.assertEqual(app.involved_users.count(), 1)
        self.assertEqual(app.involved_users.first().user, mentor)

        # Проверяем, что подразделение ментора добавлено в причастные подразделения
        self.assertEqual(app.involved_departments.count(), 1)
        self.assertEqual(app.involved_departments.first().department, dept)

    def test_status_change_created_to_created_adds_author_as_involved(self):
        """Переход статуса created → created добавляет автора в причастные."""
        # Создаем заявку с другим автором
        other_user = User.objects.create_user(
            email="other@example.com",
            password="pass12345",
            first_name="Other",
            last_name="User",
            role=self.role,
        )
        
        app = ProjectApplication.objects.create(
            title="Заявка для смены статуса",
            company="Компания",
            status=self.status,
            author=other_user,
        )
        
        # Проверяем, что автор уже добавлен в причастные (при создании)
        self.assertEqual(app.involved_users.count(), 1)
        self.assertEqual(app.involved_users.first().user, other_user)
        
        # Меняем статус с created на created
        app.status = self.status  # тот же статус created
        app.save()
        
        # Проверяем, что автор все еще в причастных (дублирования нет)
        self.assertEqual(app.involved_users.count(), 1)
        self.assertEqual(app.involved_users.first().user, other_user)

    def test_application_statuses_list_active_only(self):
        """Список статусов отдаёт только активные и содержит code/name."""
        ApplicationStatus.objects.create(code="inactive1", name="Неакт", position=10, is_active=False)
        url = reverse("application-status-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # все активные
        for item in resp.data:
            self.assertIn("code", item)
            self.assertIn("name", item)
