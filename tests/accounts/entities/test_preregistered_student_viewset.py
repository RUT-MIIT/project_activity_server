"""Тесты API предрегистрации студентов."""

from __future__ import annotations

from typing import Any

from django.core import mail
from django.test import override_settings
import pytest
from rest_framework.test import APIClient

from accounts.models import PreRegisteredStudent
from showcase.models import Institute
from teams.models import Direction, StudyGroup

LOOKUP_URL = "/api/accounts/pre-registered-students/lookup/"
REGISTER_URL = "/api/accounts/pre-registered-students/register/"
MISMATCH_URL = "/api/accounts/pre-registered-students/report-mismatch/"


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def study_group(db: Any) -> StudyGroup:
    institute = Institute.objects.create(
        code="AGA",
        name="Академия гражданской авиации",
        position=1,
        is_active=True,
    )
    direction = Direction.objects.create(
        code="25.03.03",
        name="Аэронавигация",
        level=Direction.Level.BAKALAVRIAT,
    )
    return StudyGroup.objects.create(
        name="АМБ-211",
        code="АМБ-2025-11",
        enrollment_year=2025,
        course_number=2,
        direction=direction,
        institute=institute,
    )


@pytest.fixture
def pre_registered_student(study_group: StudyGroup) -> PreRegisteredStudent:
    return PreRegisteredStudent.objects.create(
        last_name="Иванов",
        first_name="Иван",
        middle_name="Иванович",
        student_card="25011884",
        snils="18457362806",
        personnel_number="1335090",
        group=study_group,
    )


@pytest.mark.django_db
class TestPreRegisteredStudentLookup:
    def test_lookup_by_student_card(
        self, api_client: APIClient, pre_registered_student: PreRegisteredStudent
    ) -> None:
        response = api_client.post(
            LOOKUP_URL, {"student_card": "25011884"}, format="json"
        )

        assert response.status_code == 200
        assert response.data["last_name"] == "Иванов"
        assert response.data["group_name"] == "АМБ-211"
        assert response.data["student_card"] == "25011884"
        assert response.data["is_registered"] is False

    def test_lookup_by_personnel_number(
        self, api_client: APIClient, pre_registered_student: PreRegisteredStudent
    ) -> None:
        response = api_client.post(
            LOOKUP_URL, {"personnel_number": "1335090"}, format="json"
        )

        assert response.status_code == 200
        assert response.data["id"] == pre_registered_student.pk

    def test_lookup_by_snils_normalized(
        self, api_client: APIClient, pre_registered_student: PreRegisteredStudent
    ) -> None:
        response = api_client.post(
            LOOKUP_URL, {"snils": "184-573-628 06"}, format="json"
        )

        assert response.status_code == 200
        assert response.data["id"] == pre_registered_student.pk

    def test_lookup_not_found(self, api_client: APIClient) -> None:
        response = api_client.post(
            LOOKUP_URL, {"student_card": "00000000"}, format="json"
        )

        assert response.status_code == 404
        assert response.data["detail"] == "Студент не найден"

    def test_lookup_requires_single_identifier(self, api_client: APIClient) -> None:
        response = api_client.post(
            LOOKUP_URL,
            {"student_card": "25011884", "snils": "18457362806"},
            format="json",
        )

        assert response.status_code == 400


@pytest.mark.django_db
class TestPreRegisteredStudentRegister:
    def test_register_creates_user_and_returns_tokens(
        self,
        api_client: APIClient,
        pre_registered_student: PreRegisteredStudent,
        roles: dict[str, Any],
    ) -> None:
        response = api_client.post(
            REGISTER_URL,
            {
                "id": pre_registered_student.pk,
                "email": "student@example.com",
                "password": "StrongPass123!",
            },
            format="json",
        )

        assert response.status_code == 201
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["user"]["email"] == "student@example.com"

        pre_registered_student.refresh_from_db()
        assert pre_registered_student.student is not None
        assert (
            pre_registered_student.student.study_group_id
            == pre_registered_student.group_id
        )

    def test_register_already_registered(
        self,
        api_client: APIClient,
        pre_registered_student: PreRegisteredStudent,
        make_user,
        roles: dict[str, Any],
    ) -> None:
        pre_registered_student.student = make_user(
            role_code="user", email="existing@example.com"
        )
        pre_registered_student.save(update_fields=["student"])

        response = api_client.post(
            REGISTER_URL,
            {
                "id": pre_registered_student.pk,
                "email": "new@example.com",
                "password": "StrongPass123!",
            },
            format="json",
        )

        assert response.status_code == 400
        assert "уже зарегистрирован" in response.data["detail"]

    def test_register_duplicate_email(
        self,
        api_client: APIClient,
        pre_registered_student: PreRegisteredStudent,
        make_user,
        roles: dict[str, Any],
    ) -> None:
        make_user(role_code="user", email="taken@example.com")

        response = api_client.post(
            REGISTER_URL,
            {
                "id": pre_registered_student.pk,
                "email": "taken@example.com",
                "password": "StrongPass123!",
            },
            format="json",
        )

        assert response.status_code == 400
        assert "email" in response.data["detail"].lower()


@pytest.mark.django_db
class TestPreRegisteredStudentMismatch:
    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_report_mismatch_sends_email(
        self,
        api_client: APIClient,
        pre_registered_student: PreRegisteredStudent,
        settings,
    ) -> None:
        settings.ADMIN_EMAIL = "admin@example.com"

        response = api_client.post(
            MISMATCH_URL,
            {
                "id": pre_registered_student.pk,
                "comment": "У меня другая группа",
            },
            format="json",
        )

        assert response.status_code == 200
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == ["admin@example.com"]
        assert "У меня другая группа" in mail.outbox[0].body
        assert "Иванов" in mail.outbox[0].body

    def test_report_mismatch_without_admin_email(
        self,
        api_client: APIClient,
        pre_registered_student: PreRegisteredStudent,
        settings,
    ) -> None:
        settings.ADMIN_EMAIL = ""

        response = api_client.post(
            MISMATCH_URL,
            {
                "id": pre_registered_student.pk,
                "comment": "Неверные данные",
            },
            format="json",
        )

        assert response.status_code == 400
        assert "ADMIN_EMAIL" in response.data["detail"]
