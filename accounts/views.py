from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from rest_framework import decorators, permissions, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Department, RegistrationRequest, Role, User
from .serializers import (
    ApproveRequestSerializer,
    DepartmentSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
    RegistrationRequestCreateSerializer,
    RegistrationRequestSerializer,
    RejectRequestSerializer,
    RoleSerializer,
    UserSerializer,
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Используем select_related для оптимизации
        user = User.objects.select_related("department", "role").get(pk=self.user.pk)
        data["user"] = UserSerializer(user).data
        return data


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class UserMeView(APIView):
    def get(self, request):
        # Используем prefetch_related для оптимизации запроса
        user = User.objects.select_related("department", "role").get(pk=request.user.pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request=request)
            return Response(
                {"detail": "Письмо с инструкциями отправлено на указанный email."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Пароль успешно изменен."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet только для чтения подразделений/кафедр.
    Доступен только для аутентифицированных пользователей.
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Role.objects.filter(is_active=True)
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "code"
    pagination_class = None


class RegistrationRequestViewSet(viewsets.ModelViewSet):
    queryset = RegistrationRequest.objects.select_related("department", "actor").all()
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ["status"]
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "create":
            return RegistrationRequestCreateSerializer
        return RegistrationRequestSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return super().get_permissions()

    @transaction.atomic
    @decorators.action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser]
    )
    def approve(self, request, pk=None):
        reg_request = self.get_object()
        if reg_request.status != RegistrationRequest.Status.SUBMITTED:
            return Response(
                {"detail": "Заявка уже обработана."}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ApproveRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role_id = serializer.validated_data["role_id"]
        department_override = serializer.validated_data.get("department_id")
        try:
            role = Role.objects.get(pk=role_id)
        except Role.DoesNotExist:
            return Response(
                {"detail": "Роль не найдена."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_model = get_user_model()
        # Проверка: пользователь с таким email уже существует
        if user_model.objects.filter(email=reg_request.email).exists():
            return Response(
                {"detail": "Пользователь с таким email уже существует."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        password = get_random_string(12)
        assigned_department = department_override or reg_request.department
        user_model.objects.create_user(
            email=reg_request.email,
            password=password,
            first_name=reg_request.first_name,
            last_name=reg_request.last_name,
            middle_name=reg_request.middle_name,
            role=role,
            department=assigned_department,
            phone=reg_request.phone,
        )

        # Обновим департамент и роль в самой заявке, если были указаны
        reg_request.department = assigned_department
        reg_request.role = role
        reg_request.status = RegistrationRequest.Status.APPROVED
        reg_request.actor = request.user
        reg_request.save(
            update_fields=["department", "role", "status", "actor", "updated_at"]
        )

        # Отправка письма пользователю
        subject = render_to_string("registration/approved_subject.txt").strip()
        message = render_to_string(
            "registration/approved_body.txt",
            {
                "last_name": reg_request.last_name,
                "first_name": reg_request.first_name,
                "email": reg_request.email,
                "password": password,
            },
        )
        try:
            mail.send_mail(
                subject=subject,
                message=message,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                recipient_list=[reg_request.email],
                fail_silently=False,
            )
        except Exception as exc:
            # Откатим транзакцию: пользователь и изменение заявки не должны сохраниться
            transaction.set_rollback(True)
            return Response(
                {
                    "detail": (
                        "Не удалось отправить письмо пользователю. "
                        "Одобрение отменено."
                    ),
                    "error": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_data = RegistrationRequestSerializer(reg_request).data
        # В ответ добавляем сведения о назначенной роли
        response_data["role"] = RoleSerializer(role).data
        return Response(response_data, status=status.HTTP_200_OK)

    @transaction.atomic
    @decorators.action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser]
    )
    def reject(self, request, pk=None):
        reg_request = self.get_object()
        if reg_request.status != RegistrationRequest.Status.SUBMITTED:
            return Response(
                {"detail": "Заявка уже обработана."}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = RejectRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reason = serializer.validated_data.get("reason") or ""

        reg_request.status = RegistrationRequest.Status.REJECTED
        reg_request.actor = request.user
        reg_request.reason = reason
        reg_request.save(update_fields=["status", "actor", "reason", "updated_at"])

        subject = render_to_string("registration/rejected_subject.txt").strip()
        message = render_to_string(
            "registration/rejected_body.txt",
            {
                "last_name": reg_request.last_name,
                "first_name": reg_request.first_name,
                "reason": reason,
            },
        )
        mail.send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[reg_request.email],
            fail_silently=False,
        )

        return Response(
            RegistrationRequestSerializer(reg_request).data,
            status=status.HTTP_200_OK,
        )
