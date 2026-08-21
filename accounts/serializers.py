from typing import Any, Dict

from allauth.account.adapter import get_adapter
from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordResetForm as _PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers

from showcase.models import Institute

from .models import (
    AcademicYear,
    Department,
    PreRegisteredStudent,
    RegistrationRequest,
    Role,
    Semester,
    User,
)


class DepartmentSerializer(serializers.ModelSerializer):
    """Сериализатор для подразделений/кафедр."""

    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "short_name",
        ]


class RoleSerializer(serializers.ModelSerializer):
    """Сериализатор для ролей пользователей."""

    class Meta:
        model = Role
        fields = [
            "code",
            "name",
            "requires_department",
            "is_active",
        ]


class AcademicYearSerializer(serializers.ModelSerializer):
    """Сериализатор учебного года (краткий)."""

    class Meta:
        model = AcademicYear
        fields = ["id", "code", "name"]


class SemesterSerializer(serializers.ModelSerializer):
    """Сериализатор для семестров."""

    is_active = serializers.SerializerMethodField()
    academic_year = AcademicYearSerializer(read_only=True)
    academic_year_id = serializers.PrimaryKeyRelatedField(
        queryset=AcademicYear.objects.all(),
        source="academic_year",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Semester
        fields = [
            "id",
            "code",
            "name",
            "position",
            "is_active",
            "academic_year",
            "academic_year_id",
        ]
        read_only_fields = ["is_active"]

    def get_is_active(self, obj: Semester) -> bool:
        active_code = self.context.get("active_semester_code")
        return bool(active_code and obj.code == active_code)


class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    institute_code = serializers.SerializerMethodField()
    study_group = serializers.SerializerMethodField()
    student_card = serializers.SerializerMethodField()
    personnel_number = serializers.SerializerMethodField()
    snils = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "role",
            "phone",
            "department",
            "institute_code",
            "study_group",
            "student_card",
            "personnel_number",
            "snils",
        )

    @staticmethod
    def _is_student(obj: User) -> bool:
        """Проверяет, что у пользователя роль student."""
        role = getattr(obj, "role", None)
        return bool(role and role.code == "student")

    @staticmethod
    def _get_pre_registration(obj: User) -> PreRegisteredStudent | None:
        """Возвращает предрегистрацию пользователя, если она есть."""
        cache = getattr(obj, "_prefetched_objects_cache", None)
        if cache is not None and "pre_registration" in cache:
            items = cache["pre_registration"]
            return items[0] if items else None
        return obj.pre_registration.first()

    def get_institute_code(self, obj: User) -> str | None:
        """Возвращает код института пользователя.

        Приоритет: институт подразделения, затем институт учебной группы.
        """
        department = getattr(obj, "department", None)
        if department:
            institute = (
                Institute.objects.filter(department=department, is_active=True)
                .order_by("position")
                .only("code")
                .first()
            )
            if institute:
                return institute.code

        study_group = getattr(obj, "study_group", None)
        if study_group is not None and study_group.institute_id:
            return study_group.institute.code
        return None

    def get_study_group(self, obj: User) -> dict[str, Any] | None:
        """Возвращает учебную группу пользователя или None."""
        group = getattr(obj, "study_group", None)
        if group is None:
            return None

        direction = getattr(group, "direction", None)
        institute = getattr(group, "institute", None)
        return {
            "id": group.id,
            "name": group.name,
            "code": group.code,
            "enrollment_year": group.enrollment_year,
            "course_number": group.course_number,
            "is_end": group.is_end,
            "profile": group.profile,
            "form": group.form,
            "direction": (
                {
                    "code": direction.code,
                    "level": direction.level,
                    "name": direction.name,
                }
                if direction is not None
                else None
            ),
            "institute": (
                {
                    "code": institute.code,
                    "name": institute.name,
                }
                if institute is not None
                else None
            ),
        }

    def get_student_card(self, obj: User) -> str | None:
        """Возвращает номер студенческого билета для роли student."""
        if not self._is_student(obj):
            return None
        pre_registered = self._get_pre_registration(obj)
        return pre_registered.student_card if pre_registered else None

    def get_personnel_number(self, obj: User) -> str | None:
        """Возвращает табельный номер для роли student."""
        if not self._is_student(obj):
            return None
        pre_registered = self._get_pre_registration(obj)
        return pre_registered.personnel_number if pre_registered else None

    def get_snils(self, obj: User) -> str | None:
        """Возвращает СНИЛС для роли student."""
        if not self._is_student(obj):
            return None
        pre_registered = self._get_pre_registration(obj)
        if pre_registered is None:
            return None
        return pre_registered.snils or None


class UserUpdateSerializer(serializers.Serializer):
    """Сериализатор частичного обновления пользователя."""

    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.filter(is_active=True),
        required=False,
    )
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source="department",
        required=False,
        allow_null=True,
    )
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(
        max_length=20,
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    def validate_email(self, value: str) -> str:
        """Проверяет уникальность email с учётом обновляемого пользователя."""
        normalized_email = User.objects.normalize_email(value)
        user_id = self.context.get("user_id")
        queryset = User.objects.filter(email=normalized_email)
        if user_id is not None:
            queryset = queryset.exclude(pk=user_id)
        if queryset.exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует."
            )
        return normalized_email


class CustomResetPasswordForm(_PasswordResetForm):
    def save(self, request=None, **kwargs):
        email = self.cleaned_data["email"]
        token_generator = kwargs.get("token_generator", default_token_generator)
        template = kwargs.get("email_template_name")
        extra = kwargs.get("extra_email_context", {})
        for user in self.get_users(email):
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            reset_url = f"{settings.FRONT_END}/reset_password/{uid}/{token}"
            context = {
                "user": user,
                "request": request,
                "email": email,
                "reset_url": reset_url,
            }
            context.update(extra)
            get_adapter(request).send_mail(template, email, context)
        return email


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    @property
    def password_reset_form_class(self):
        return CustomResetPasswordForm

    def get_email_options(self):
        return {"email_template_name": "password/password_reset.html"}

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email не найден.")
        return value

    def save(self, request):
        opts = self.get_email_options()
        form = self.password_reset_form_class(data=self.validated_data)
        if form.is_valid():
            form.save(request=request, **opts)
        else:
            raise serializers.ValidationError(form.errors)


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            uid = urlsafe_base64_decode(attrs["uid"]).decode()
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError(
                "Некорректная ссылка для сброса пароля."
            ) from None
        if not default_token_generator.check_token(self.user, attrs["token"]):
            raise serializers.ValidationError(
                "Ссылка для сброса пароля недействительна или устарела."
            )
        return attrs

    def save(self) -> User:
        self.user.set_password(self.validated_data["new_password"])
        self.user.save()
        return self.user


class PasswordChangeSerializer(serializers.Serializer):
    """Сериализатор для смены пароля аутентифицированного пользователя."""

    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        user = self.context.get("request").user
        if user is None or not user.is_authenticated:
            raise serializers.ValidationError("Пользователь не аутентифицирован.")

        if not user.check_password(attrs["current_password"]):
            raise serializers.ValidationError(
                {"current_password": "Неверный текущий пароль."}
            )

        password_validation.validate_password(attrs["new_password"], user)
        return attrs

    def save(self, **kwargs: Any) -> User:
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        return user


class UserShortSerializer(serializers.ModelSerializer):
    """Краткий сериализатор пользователя для отображения в других сущностях."""

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "full_name"]

    def get_full_name(self, obj):
        parts = [obj.last_name, obj.first_name, getattr(obj, "middle_name", "")]
        return " ".join([p for p in parts if p]).strip()


class RegistrationRequestCreateSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=True
    )

    class Meta:
        model = RegistrationRequest
        fields = [
            "id",
            "last_name",
            "first_name",
            "middle_name",
            "department",
            "email",
            "phone",
            "comment",
            "created_at",
            "status",
        ]
        read_only_fields = ["id", "created_at", "status"]

    def validate_email(self, value: str) -> str:
        """Проверяет email: нормализация, отсутствие пользователя и активной заявки."""
        normalized_email = User.objects.normalize_email(value)

        if User.objects.filter(email=normalized_email).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже зарегистрирован."
            )

        if RegistrationRequest.objects.filter(
            email=normalized_email, status=RegistrationRequest.Status.SUBMITTED
        ).exists():
            raise serializers.ValidationError(
                "Заявка с таким email уже подана и ожидает обработки."
            )

        return normalized_email

    def validate_department(self, value):
        """Валидация подразделения."""
        if value is None:
            raise serializers.ValidationError("Подразделение обязательно для указания.")
        return value


class RegistrationRequestSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    actor = UserShortSerializer(read_only=True)
    role = RoleSerializer(read_only=True)

    class Meta:
        model = RegistrationRequest
        fields = [
            "id",
            "last_name",
            "first_name",
            "middle_name",
            "department",
            "email",
            "phone",
            "comment",
            "reason",
            "role",
            "status",
            "actor",
            "created_at",
            "updated_at",
        ]


class ApproveRequestSerializer(serializers.Serializer):
    role_id = serializers.CharField()
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False, allow_null=True
    )

    def validate_role_id(self, value):
        try:
            Role.objects.get(pk=value)
        except Role.DoesNotExist:
            raise serializers.ValidationError("Роль не найдена.") from None
        return value


class RejectRequestSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class PreRegisteredStudentLookupSerializer(serializers.Serializer):
    """Поиск предрегистрации по одному идентификатору."""

    student_card = serializers.CharField(required=False, allow_blank=True)
    personnel_number = serializers.CharField(required=False, allow_blank=True)
    snils = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        provided = {
            key: (attrs.get(key) or "").strip()
            for key in ("student_card", "personnel_number", "snils")
        }
        non_empty = [key for key, value in provided.items() if value]
        if len(non_empty) != 1:
            raise serializers.ValidationError(
                "Укажите ровно одно поле: student_card, personnel_number или snils."
            )
        attrs.update(provided)
        return attrs


class PreRegisteredStudentLookupResponseSerializer(serializers.Serializer):
    """Ответ поиска предрегистрации."""

    id = serializers.IntegerField()
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    middle_name = serializers.CharField()
    group_name = serializers.CharField()
    student_card = serializers.CharField()
    is_registered = serializers.BooleanField()


class PreRegisteredStudentRegisterSerializer(serializers.Serializer):
    """Регистрация пользователя по предрегистрации."""

    id = serializers.IntegerField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)


class PreRegisteredStudentMismatchSerializer(serializers.Serializer):
    """Сообщение администратору о расхождении данных."""

    id = serializers.IntegerField()
    comment = serializers.CharField(min_length=1, trim_whitespace=True)
