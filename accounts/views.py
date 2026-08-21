from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.db import IntegrityError, transaction
from django.db.models import Prefetch
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from drf_spectacular.utils import extend_schema
from rest_framework import decorators, permissions, status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from showcase.models import Institute

from .models import Department, RegistrationRequest, Role, Semester, User
from .permissions import IsAdminOrCpds, IsCpdsUser, RegistrationRequestManagePermission
from .serializers import (
    ApproveRequestSerializer,
    DepartmentSerializer,
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
    RegistrationRequestCreateSerializer,
    RegistrationRequestSerializer,
    RejectRequestSerializer,
    RoleSerializer,
    SemesterSerializer,
    UserSerializer,
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Используем select_related и prefetch_related для оптимизации
        user = (
            User.objects.select_related(
                "department",
                "role",
                "study_group",
                "study_group__direction",
                "study_group__institute",
            )
            .prefetch_related(
                Prefetch(
                    "department__institutes",
                    queryset=Institute.objects.filter(is_active=True),
                ),
                "pre_registration",
            )
            .get(pk=self.user.pk)
        )
        data["user"] = UserSerializer(user).data
        return data


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class UserMeView(APIView):
    @extend_schema(
        tags=["accounts"], responses=UserSerializer, summary="Текущий пользователь"
    )
    def get(self, request):
        # Используем select_related и prefetch_related для оптимизации запроса
        user = (
            User.objects.select_related(
                "department",
                "role",
                "study_group",
                "study_group__direction",
                "study_group__institute",
            )
            .prefetch_related(
                Prefetch(
                    "department__institutes",
                    queryset=Institute.objects.filter(is_active=True),
                ),
                "pre_registration",
            )
            .get(pk=request.user.pk)
        )
        serializer = UserSerializer(user)
        return Response(serializer.data)


class PasswordResetView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer

    @extend_schema(tags=["accounts"], summary="Сброс пароля")
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request=request)
            return Response(
                {"detail": "Письмо с инструкциями отправлено на указанный email."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    @extend_schema(tags=["accounts"], summary="Подтверждение сброса пароля")
    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Пароль успешно изменен."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    @extend_schema(tags=["accounts"], summary="Смена пароля")
    def post(self, request: Request) -> Response:
        """
        Сменяет пароль текущего пользователя после проверки текущего пароля.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Пароль успешно изменен."}, status=status.HTTP_200_OK
        )


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet только для чтения подразделений/кафедр.

    Список подразделений должен быть доступен всем пользователям (AllowAny),
    чтобы пользователь мог выбрать своё подразделение ещё до авторизации.
    Другие действия (detail) по умолчанию требуют авторизации.
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_permissions(self):
        """Для list используем AllowAny, остальные действия требуют авторизации."""

        if self.action == "list":
            return [permissions.AllowAny()]
        return super().get_permissions()


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Role.objects.filter(is_active=True)
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "code"
    pagination_class = None


class SemesterViewSet(viewsets.ModelViewSet):
    """CRUD для семестров. Чтение — для аутентифицированных, управление — admin/cpds."""

    queryset = Semester.objects.select_related("academic_year").order_by("position")
    serializer_class = SemesterSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_serializer_context(self):
        """Один запрос к Settings на ответ — код активного семестра для is_active."""
        context = super().get_serializer_context()
        context["active_semester_code"] = Semester.get_active_code()
        return context

    def get_permissions(self):
        """Ограничиваем запись только admin/cpds, чтение — любому аутентифицированному."""

        if self.action in ["list", "retrieve"]:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdminOrCpds()]


class RegistrationRequestViewSet(viewsets.ModelViewSet):
    queryset = RegistrationRequest.objects.select_related("department", "actor").all()
    permission_classes = [RegistrationRequestManagePermission]
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

    def create(self, request, *args, **kwargs):
        """Создание заявки с обработкой гонки при параллельных запросах."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except IntegrityError:
            return Response(
                {"email": ["Заявка с таким email уже подана и ожидает обработки."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @transaction.atomic
    @decorators.action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAdminUser | IsCpdsUser],
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
                "front_end": settings.FRONT_END.rstrip("/"),
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
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAdminUser | IsCpdsUser],
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
        try:
            mail.send_mail(
                subject=subject,
                message=message,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                recipient_list=[reg_request.email],
                fail_silently=False,
            )
        except Exception as exc:
            # Не считаем ошибку отправки письма критичной для отклонения заявки.
            # Статус уже изменён на REJECTED, поэтому просто возвращаем успешный ответ
            # с дополнительной информацией об ошибке доставки письма.
            response_data = RegistrationRequestSerializer(reg_request).data
            response_data["email_error"] = str(exc)
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(
            RegistrationRequestSerializer(reg_request).data,
            status=status.HTTP_200_OK,
        )
