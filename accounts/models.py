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
    is_placeholder = models.BooleanField(
        default=False,
        verbose_name="Псевдо-аккаунт контингента",
    )
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
    study_group = models.ForeignKey(
        "teams.StudyGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="Учебная группа",
    )
    position = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Должность",
    )
    academic_degree = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Учёная степень",
    )
    academic_title = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Учёное звание",
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


class UserWithEmailProvision(User):
    """Proxy-модель для отдельного admin-интерфейса создания пользователя с письмом."""

    class Meta:
        proxy = True
        verbose_name = "Создать пользователя (с письмом)"
        verbose_name_plural = "Создать пользователя (с письмом)"


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
    email = models.EmailField(verbose_name="Email")
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
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                condition=models.Q(status="submitted"),
                name="unique_submitted_registration_email",
            ),
        ]

    def __str__(self):
        return f"{self.last_name} {self.first_name} <{self.email}> [{self.status}]"


class PreRegisteredStudent(models.Model):
    """Предрегистрация пользователя (студент или наставник)."""

    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    middle_name = models.CharField(
        max_length=150, blank=True, default="", verbose_name="Отчество"
    )
    role = models.ForeignKey(
        "Role",
        on_delete=models.PROTECT,
        default="student",
        related_name="pre_registrations",
        verbose_name="Роль",
        db_index=True,
    )
    student_card = models.CharField(
        max_length=32,
        blank=True,
        default="",
        db_index=True,
        verbose_name="Студенческий билет",
    )
    snils = models.CharField(
        max_length=11,
        blank=True,
        default="",
        db_index=True,
        verbose_name="СНИЛС",
    )
    personnel_number = models.CharField(
        max_length=32,
        unique=True,
        db_index=True,
        verbose_name="Табельный номер (ID_E человека)",
    )
    department = models.ForeignKey(
        "Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pre_registrations",
        verbose_name="Подразделение",
    )
    group = models.ForeignKey(
        "teams.StudyGroup",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="pre_registered_students",
        verbose_name="Учебная группа",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pre_registration",
        verbose_name="Зарегистрированный пользователь",
    )
    has_placeholder_user = models.BooleanField(
        default=False,
        verbose_name="Создан псевдо-аккаунт",
    )

    class Meta:
        verbose_name = "Предрегистрация"
        verbose_name_plural = "Предрегистрации"
        ordering = ("last_name", "first_name")
        constraints = [
            models.UniqueConstraint(
                fields=["snils"],
                condition=~models.Q(snils=""),
                name="unique_preregistered_student_snils",
            ),
            models.UniqueConstraint(
                fields=["student_card"],
                condition=~models.Q(student_card=""),
                name="unique_preregistered_student_card",
            ),
        ]

    def __str__(self) -> str:
        if self.student_card:
            return (
                f"{self.last_name} {self.first_name} "
                f"(билет {self.student_card}, таб. {self.personnel_number})"
            )
        return f"{self.last_name} {self.first_name} (таб. {self.personnel_number})"

    @property
    def is_registered(self) -> bool:
        """Возвращает True, если пользователь прошёл полную регистрацию (не псевдо-user)."""
        return self.user_id is not None and not self.has_placeholder_user


class AcademicYear(models.Model):
    """Учебный год."""

    code = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="Код",
    )
    name = models.CharField(max_length=255, verbose_name="Название")

    class Meta:
        verbose_name = "Учебный год"
        verbose_name_plural = "Учебные годы"
        ordering = ("code",)

    def __str__(self) -> str:
        return f"{self.code} — {self.name}"


class Settings(models.Model):
    """Ключ–значение настроек приложения (редактируемые из админки / импортом)."""

    code = models.CharField(
        max_length=128,
        unique=True,
        verbose_name="Код",
    )
    description = models.CharField(
        max_length=512,
        blank=True,
        default="",
        verbose_name="Описание",
    )
    value = models.TextField(blank=True, default="", verbose_name="Значение")

    class Meta:
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"

    def __str__(self) -> str:
        return self.code


ACTIVE_SEMESTER_SETTING_CODE = "active_semester_code"
NEXT_SEMESTER_SETTING_CODE = "next_semester_code"


class Semester(models.Model):
    code = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        verbose_name="Код",
    )
    name = models.CharField(max_length=255, verbose_name="Название семестра")
    position = models.PositiveIntegerField(verbose_name="Позиция для сортировки")
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="semesters",
        verbose_name="Учебный год",
    )

    class Meta:
        verbose_name = "Семестр"
        verbose_name_plural = "Семестры"
        ordering = ["position"]

    def __str__(self) -> str:
        return f"{self.code} — {self.name}"

    @classmethod
    def _setting_value(cls, setting_code: str) -> str | None:
        try:
            setting = Settings.objects.get(code=setting_code)
        except Settings.DoesNotExist:
            return None
        code = (setting.value or "").strip()
        return code or None

    @classmethod
    def get_active_code(cls) -> str | None:
        """Код текущего активного семестра (Settings.active_semester_code)."""
        return cls._setting_value(ACTIVE_SEMESTER_SETTING_CODE)

    @classmethod
    def _from_setting_code(cls, setting_code: str) -> "Semester | None":
        code = cls._setting_value(setting_code)
        if not code:
            return None
        return cls.objects.filter(code=code).first()

    @classmethod
    def get_active(cls) -> "Semester | None":
        """Текущий активный семестр (Settings.active_semester_code)."""
        return cls._from_setting_code(ACTIVE_SEMESTER_SETTING_CODE)

    @classmethod
    def get_next(cls) -> "Semester | None":
        """Следующий семестр для новых заявок (Settings.next_semester_code)."""
        return cls._from_setting_code(NEXT_SEMESTER_SETTING_CODE)

    @classmethod
    def resolve_list_semester_id(cls, raw: str | None) -> int:
        """Разбор query-параметра semester_id для GET-списков: id, next, actual."""
        if raw is None:
            raise ValueError("semester_id не передан")
        value = raw.strip()
        if not value:
            raise ValueError("Параметр semester_id не может быть пустым")

        lowered = value.lower()
        if lowered == "next":
            semester = cls.get_next()
            if semester is None:
                raise ValueError(
                    "Семестр next не настроен (проверьте next_semester_code)"
                )
            return semester.pk
        if lowered == "actual":
            semester = cls.get_active()
            if semester is None:
                raise ValueError(
                    "Семестр actual не настроен (проверьте active_semester_code)"
                )
            return semester.pk

        try:
            pk = int(value)
        except ValueError as err:
            raise ValueError(
                f"semester_id должен быть числом, 'next' или 'actual', получено: {raw!r}"
            ) from err
        if pk <= 0:
            raise ValueError(f"Некорректный semester_id: {pk}")
        if not cls.objects.filter(pk=pk).exists():
            raise ValueError(f"Семестр с id={pk} не найден")
        return pk
