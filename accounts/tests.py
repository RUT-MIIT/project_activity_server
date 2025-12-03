from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase, override_settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APIClient

from .models import Department, RegistrationRequest, Role


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class AccountsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_model = get_user_model()

        # Создаем базовые данные
        self.role_admin = Role.objects.create(
            code="admin",
            name="Администратор",
            requires_department=False,
            is_active=True,
        )
        self.role_user = Role.objects.create(
            code="user", name="Пользователь", requires_department=False, is_active=True
        )
        self.dept = Department.objects.create(name="Кафедра тестов", short_name="KT")

        self.role_cpds = Role.objects.create(
            code="cpds", name="ЦПДС", requires_department=False, is_active=True
        )

        # Админ
        self.admin_password = "AdminPass123!"
        self.admin = self.user_model.objects.create_user(
            email="admin@example.com",
            password=self.admin_password,
            first_name="Admin",
            last_name="User",
            role=self.role_admin,
            department=self.dept,
        )
        self.admin.is_staff = True
        self.admin.save(update_fields=["is_staff"])

        # Обычный пользователь
        self.user_password = "UserPass123!"
        self.user = self.user_model.objects.create_user(
            email="user@example.com",
            password=self.user_password,
            first_name="Regular",
            last_name="User",
            role=self.role_user,
            department=self.dept,
        )

        # Пользователь ЦПДС
        self.cpds_password = "CpdsPass123!"
        self.cpds_user = self.user_model.objects.create_user(
            email="cpds@example.com",
            password=self.cpds_password,
            first_name="Cpds",
            last_name="User",
            role=self.role_cpds,
            department=self.dept,
        )

    def auth(self, email, password):
        """Логинится и проставляет Bearer-токен в заголовках клиента."""
        url = "/api/accounts/login/"
        response = self.client.post(
            url, {"email": email, "password": password}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_login_returns_tokens_and_user(self):
        """Проверяет, что логин возвращает access/refresh токены и данные пользователя."""
        url = "/api/accounts/login/"
        response = self.client.post(
            url,
            {"email": self.user.email, "password": self.user_password},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)

    def test_user_me_requires_auth_and_returns_profile(self):
        """Без токена возвращается 401, с токеном — профиль текущего пользователя."""
        # Без авторизации
        url = "/api/accounts/user/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

        # С авторизацией
        self.auth(self.user.email, self.user_password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], self.user.email)

    def test_password_reset_sends_email(self):
        """Сброс пароля по email отправляет письмо (locmem backend)."""
        url = "/api/accounts/password/reset/"
        response = self.client.post(url, {"email": self.user.email}, format="json")
        self.assertEqual(response.status_code, 200)
        # Проверяем, что письмо попало в outbox
        self.assertGreaterEqual(len(mail.outbox), 1)

    def test_password_reset_confirm_changes_password(self):
        """Подтверждение сброса пароля меняет пароль и позволяет войти новым паролем."""
        # Генерируем токен
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        url = "/api/accounts/password/reset/confirm/"
        new_password = "NewPass123!"
        response = self.client.post(
            url,
            {"uid": uid, "token": token, "new_password": new_password},
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        # Проверяем, что можно залогиниться новым паролем
        login_resp = self.client.post(
            "/api/accounts/login/",
            {"email": self.user.email, "password": new_password},
            format="json",
        )
        self.assertEqual(login_resp.status_code, 200)

    def test_departments_list_allow_any_detail_requires_auth(self):
        """Список департаментов доступен всем, детальный просмотр требует авторизации."""
        # List доступен всем (AllowAny)
        list_url = "/api/accounts/departments/"
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

        # Retrieve без авторизации запрещён
        detail_url = f"/api/accounts/departments/{self.dept.id}/"
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 401)

        # С авторизацией доступ разрешён
        self.auth(self.user.email, self.user_password)
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.dept.id)

    def test_registration_request_create_anonymous_allowed(self):
        """Аноним может создать заявку на регистрацию и она сохраняется в БД."""
        url = "/api/accounts/registration-requests/"
        payload = {
            "last_name": "Иванов",
            "first_name": "Иван",
            "middle_name": "Иванович",
            "department": self.dept.id,
            "email": "new_user@example.com",
            "phone": "+79990000000",
            "comment": "Хочу доступ",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            RegistrationRequest.objects.filter(email="new_user@example.com").exists()
        )

    def test_registration_request_create_requires_department(self):
        """Создание заявки без подразделения возвращает ошибку валидации."""
        url = "/api/accounts/registration-requests/"
        payload = {
            "last_name": "Иванов",
            "first_name": "Иван",
            "middle_name": "Иванович",
            "email": "no_dept@example.com",
            "phone": "+79990000000",
            "comment": "Хочу доступ",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("department", response.data)

    def test_registration_request_create_invalid_department(self):
        """Создание заявки с несуществующим подразделением возвращает ошибку валидации."""
        url = "/api/accounts/registration-requests/"
        payload = {
            "last_name": "Иванов",
            "first_name": "Иван",
            "middle_name": "Иванович",
            "department": 99999,  # Несуществующий ID
            "email": "invalid_dept@example.com",
            "phone": "+79990000000",
            "comment": "Хочу доступ",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("department", response.data)

    def test_registration_request_list_requires_privileged_user(self):
        """Список заявок доступен только is_staff, admin или cpds."""
        url = "/api/accounts/registration-requests/"
        # Без авторизации
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        # Под обычным пользователем
        self.auth(self.user.email, self.user_password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Под пользователем ЦПДС
        self.client = APIClient()  # сбрасываем креды
        self.auth(self.cpds_user.email, self.cpds_password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Под админом
        self.client = APIClient()
        self.auth(self.admin.email, self.admin_password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_registration_request_approve_creates_user_and_sends_email(self):
        """Админ утверждает заявку: создаётся пользователь и отправляется письмо."""
        # Создаем заявку
        reg = RegistrationRequest.objects.create(
            last_name="Петров",
            first_name="Петр",
            middle_name="",
            department=self.dept,
            email="petrov@example.com",
            phone="+79991112233",
            comment="-",
        )
        # Админ утверждает
        self.client = APIClient()
        self.auth(self.admin.email, self.admin_password)
        url = f"/api/accounts/registration-requests/{reg.id}/approve/"
        payload = {"role_id": self.role_user.code}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 200)
        # Пользователь создан
        self.assertTrue(
            self.user_model.objects.filter(email="petrov@example.com").exists()
        )
        # Письмо отправлено
        self.assertGreaterEqual(len(mail.outbox), 1)
        # В ответе присутствует роль назначенного пользователя
        self.assertIn("role", response.data)
        self.assertEqual(response.data["role"]["code"], self.role_user.code)
        # В самой заявке сохранена роль
        reg.refresh_from_db()
        self.assertIsNotNone(reg.role)
        self.assertEqual(reg.role.code, self.role_user.code)

    def test_registration_request_reject_changes_status_and_sends_email(self):
        """Админ отклоняет заявку: статус становится REJECTED и уходит письмо."""
        reg = RegistrationRequest.objects.create(
            last_name="Сидоров",
            first_name="Сидор",
            middle_name="",
            department=self.dept,
            email="sidorov@example.com",
            phone="+79995557788",
            comment="-",
        )
        self.client = APIClient()
        self.auth(self.admin.email, self.admin_password)
        url = f"/api/accounts/registration-requests/{reg.id}/reject/"
        payload = {"reason": "Недостаточно данных"}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 200)
        reg.refresh_from_db()
        self.assertEqual(reg.status, RegistrationRequest.Status.REJECTED)
        self.assertGreaterEqual(len(mail.outbox), 1)

    def test_registration_request_approve_forbidden_for_regular_user(self):
        """Обычный пользователь не может утверждать заявки (ожидается 403)."""
        reg = RegistrationRequest.objects.create(
            last_name="Иванов",
            first_name="Иван",
            middle_name="",
            department=self.dept,
            email="ivanov@example.com",
            phone="+79990001122",
            comment="-",
        )
        # Авторизуемся обычным пользователем
        self.client = APIClient()
        self.auth(self.user.email, self.user_password)
        url = f"/api/accounts/registration-requests/{reg.id}/approve/"
        payload = {"role_id": self.role_user.code}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 403)

    def test_registration_request_reject_forbidden_for_regular_user(self):
        """Обычный пользователь не может отклонять заявки (ожидается 403)."""
        reg = RegistrationRequest.objects.create(
            last_name="Иванов",
            first_name="Иван",
            middle_name="",
            department=self.dept,
            email="ivanov2@example.com",
            phone="+79990003344",
            comment="-",
        )
        self.client = APIClient()
        self.auth(self.user.email, self.user_password)
        url = f"/api/accounts/registration-requests/{reg.id}/reject/"
        payload = {"reason": "Нет прав"}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 403)

    def test_registration_request_approve_allowed_for_cpds_user(self):
        """Пользователь ЦПДС может утверждать заявки (IsCpdsUser)."""
        reg = RegistrationRequest.objects.create(
            last_name="Ковалёв",
            first_name="Кирилл",
            middle_name="",
            department=self.dept,
            email="kovalev@example.com",
            phone="+79990005566",
            comment="-",
        )
        # Авторизуемся пользователем ЦПДС
        self.client = APIClient()
        self.auth(self.cpds_user.email, self.cpds_password)
        url = f"/api/accounts/registration-requests/{reg.id}/approve/"
        payload = {"role_id": self.role_user.code}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 200)
        # Пользователь создан
        self.assertTrue(
            self.user_model.objects.filter(email="kovalev@example.com").exists()
        )

    def test_registration_request_reject_allowed_for_cpds_user(self):
        """Пользователь ЦПДС может отклонять заявки (IsCpdsUser)."""
        reg = RegistrationRequest.objects.create(
            last_name="Романов",
            first_name="Роман",
            middle_name="",
            department=self.dept,
            email="romanov@example.com",
            phone="+79990007788",
            comment="-",
        )
        self.client = APIClient()
        self.auth(self.cpds_user.email, self.cpds_password)
        url = f"/api/accounts/registration-requests/{reg.id}/reject/"
        payload = {"reason": "Не подходит"}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 200)
        reg.refresh_from_db()
        self.assertEqual(reg.status, RegistrationRequest.Status.REJECTED)

    def test_registration_request_approve_mail_failure_returns_400_and_no_user_created(
        self,
    ):
        """Если отправка письма при approve падает, возвращаем 400 и не создаём пользователя."""
        reg = RegistrationRequest.objects.create(
            last_name="Почтов",
            first_name="Сбой",
            middle_name="",
            department=self.dept,
            email="bad_email@example.com",
            phone="+79990000001",
            comment="-",
        )
        # Авторизуемся админом
        self.client = APIClient()
        self.auth(self.admin.email, self.admin_password)

        # Мокаем send_mail, чтобы он бросал исключение
        from django.core import mail as core_mail

        original_send_mail = core_mail.send_mail

        def raising_send_mail(*args, **kwargs):
            raise RuntimeError("SMTP failed")

        core_mail.send_mail = raising_send_mail
        try:
            url = f"/api/accounts/registration-requests/{reg.id}/approve/"
            payload = {"role_id": self.role_user.code}
            response = self.client.post(url, payload, format="json")
            self.assertEqual(response.status_code, 400)
            self.assertIn("detail", response.data)
            # Пользователь не создан
            self.assertFalse(self.user_model.objects.filter(email=reg.email).exists())
            # Статус заявки не должен поменяться на APPROVED из-за отката
            reg.refresh_from_db()
            self.assertEqual(reg.status, RegistrationRequest.Status.SUBMITTED)
        finally:
            # Вернём исходную функцию
            core_mail.send_mail = original_send_mail

    def test_registration_request_reject_mail_failure_still_returns_200_and_keeps_rejected_status(
        self,
    ):
        """Если отправка письма при reject падает, возвращаем 200 и оставляем статус REJECTED."""
        reg = RegistrationRequest.objects.create(
            last_name="Ошибкин",
            first_name="Отказ",
            middle_name="",
            department=self.dept,
            email="broken_email@example.com",
            phone="+79990009999",
            comment="-",
        )
        # Авторизуемся админом
        self.client = APIClient()
        self.auth(self.admin.email, self.admin_password)

        # Мокаем send_mail, чтобы он бросал исключение
        from django.core import mail as core_mail

        original_send_mail = core_mail.send_mail

        def raising_send_mail(*args, **kwargs):
            raise RuntimeError("SMTP failed")

        core_mail.send_mail = raising_send_mail
        try:
            url = f"/api/accounts/registration-requests/{reg.id}/reject/"
            payload = {"reason": "Почта не работает"}
            response = self.client.post(url, payload, format="json")
            # Не должны получить 500, ожидаем 200
            self.assertEqual(response.status_code, 200)
            # Заявка должна остаться в статусе REJECTED
            reg.refresh_from_db()
            self.assertEqual(reg.status, RegistrationRequest.Status.REJECTED)
            # В ответе есть информация об ошибке отправки письма
            self.assertIn("email_error", response.data)
        finally:
            core_mail.send_mail = original_send_mail

    def test_user_roles_list_requires_auth_and_returns(self):
        """Список ролей требует авторизации и возвращает хотя бы одну роль."""
        url = "/api/accounts/roles/"
        # Без авторизации
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        # С авторизацией
        self.auth(self.user.email, self.user_password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_user_roles_retrieve_by_code(self):
        """Детальный просмотр роли по коду (lookup_field=code) требует авторизации."""
        url = f"/api/accounts/roles/{self.role_user.code}/"
        self.auth(self.user.email, self.user_password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], self.role_user.code)


from django.test import TestCase

# Create your tests here.
