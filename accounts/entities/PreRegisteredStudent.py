"""API предрегистрации студентов из контингента."""

from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from accounts.serializers import (
    PreRegisteredStudentLookupResponseSerializer,
    PreRegisteredStudentLookupSerializer,
    PreRegisteredStudentMismatchSerializer,
    PreRegisteredStudentRegisterSerializer,
)
from accounts.services.preregistered_student_service import PreRegisteredStudentService


@extend_schema_view(
    lookup=extend_schema(
        tags=["accounts"],
        request=PreRegisteredStudentLookupSerializer,
        responses={200: PreRegisteredStudentLookupResponseSerializer},
        summary="Поиск предрегистрации студента",
    ),
    register=extend_schema(
        tags=["accounts"],
        request=PreRegisteredStudentRegisterSerializer,
        summary="Регистрация студента по предрегистрации",
    ),
    report_mismatch=extend_schema(
        tags=["accounts"],
        request=PreRegisteredStudentMismatchSerializer,
        summary="Сообщить о расхождении данных",
    ),
)
class PreRegisteredStudentViewSet(viewsets.GenericViewSet):
    """Публичные операции предрегистрации студентов."""

    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "preregistered_student"

    @action(detail=False, methods=["post"], url_path="lookup")
    def lookup(self, request: Request) -> Response:
        """Ищет предрегистрацию по студбилету, табельному номеру или СНИЛС."""
        serializer = PreRegisteredStudentLookupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        service = PreRegisteredStudentService()
        result = service.lookup(
            student_card=data.get("student_card") or None,
            personnel_number=data.get("personnel_number") or None,
            snils=data.get("snils") or None,
        )
        if result is None:
            return Response(
                {"detail": "Студент не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(result.to_dict(), status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request: Request) -> Response:
        """Создаёт пользователя и возвращает JWT по данным предрегистрации."""
        serializer = PreRegisteredStudentRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        service = PreRegisteredStudentService()
        try:
            payload = service.register(
                pre_registered_id=data["id"],
                email=data["email"],
                password=data["password"],
            )
        except ValidationError as exc:
            return Response(
                {"password": exc.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except RuntimeError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(payload, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="report-mismatch")
    def report_mismatch(self, request: Request) -> Response:
        """Отправляет администратору письмо о расхождении данных."""
        serializer = PreRegisteredStudentMismatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        service = PreRegisteredStudentService()
        try:
            service.report_mismatch(
                pre_registered_id=data["id"],
                comment=data["comment"],
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"detail": "Сообщение отправлено администратору"},
            status=status.HTTP_200_OK,
        )
