from allauth.account.adapter import get_adapter
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm as _PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers

from .models import Department, RegistrationRequest, Role, User


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


class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

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
        )


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

    def validate(self, attrs):
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

    def save(self):
        self.user.set_password(self.validated_data["new_password"])
        self.user.save()
        return self.user


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

    def validate_email(self, value):
        # Не позволяем подавать повторную заявку, если уже есть с таким email в статусе submitted
        if RegistrationRequest.objects.filter(
            email=value, status=RegistrationRequest.Status.SUBMITTED
        ).exists():
            raise serializers.ValidationError(
                "Заявка с таким email уже подана и ожидает обработки."
            )
        return value

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
