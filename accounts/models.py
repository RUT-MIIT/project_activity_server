from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email должен быть указан")
        email = self.normalize_email(email)
        if not extra_fields.get("role"):
            raise ValueError("Укажите роль пользователя")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if not extra_fields.get("role"):
            from accounts.models import Role

            extra_fields["role"] = Role.objects.get(code="admin")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)
    role = models.ForeignKey(
        "Role",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Роль",
        related_name="users",
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(
        "Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="Подразделение",
    )
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Телефон"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

    def get_full_name(self):
        parts = [self.last_name, self.first_name, getattr(self, "middle_name", "")]
        return " ".join([p for p in parts if p]).strip()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Department(models.Model):
    name = models.CharField("Название подразделения", max_length=255)
    short_name = models.CharField("Краткое название", max_length=64)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родительское подразделение",
    )
    can_save_project_applications = models.BooleanField(
        default=False, verbose_name="Может сохранять проектные заявки"
    )

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"

    def __str__(self):
        return self.name


class Role(models.Model):
    code = models.CharField(max_length=50, primary_key=True, verbose_name="Код роли")
    name = models.CharField(max_length=255, verbose_name="Название роли")
    requires_department = models.BooleanField(
        default=False, verbose_name="Требует указания подразделения"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code}: {self.name}"


class RegistrationRequest(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Подана"
        APPROVED = "approved", "Одобрена"
        REJECTED = "rejected", "Отклонена"

    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    middle_name = models.CharField(max_length=150, blank=True, verbose_name="Отчество")
    department = models.ForeignKey(
        "Department",
        on_delete=models.PROTECT,
        related_name="registration_requests",
        verbose_name="Подразделение",
        null=True,
        blank=True,
    )
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=32, verbose_name="Телефон")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    reason = models.TextField(blank=True, null=True, verbose_name="Причина отказа")
    role = models.ForeignKey(
        "Role",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registration_requests",
        verbose_name="Роль (назначенная при одобрении)",
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.SUBMITTED,
        verbose_name="Статус",
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="processed_registration_requests",
        verbose_name="Изменил статус",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name = "Заявка на регистрацию"
        verbose_name_plural = "Заявки на регистрацию"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.last_name} {self.first_name} <{self.email}> [{self.status}]"
