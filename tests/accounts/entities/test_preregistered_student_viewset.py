"""Тесты API предрегистрации студентов."""

from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
import pytest
from rest_framework.test import APIClient

from accounts.models import PreRegisteredStudent, Semester, Settings
from showcase.models import Institute
from teams.models import (
    Direction,
    StudyGroup,
    StudyGroupProjectTeacher,
    StudyGroupSemester,
)

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
            LOOKUP_URL,
            {"student_card": "25011884", "last_name": "Иванов"},
            format="json",
        )

        assert response.status_code == 200
        assert response.data["last_name"] == "Иванов"
        assert response.data["role"] == "student"
        assert response.data["group_name"] == "АМБ-211"
        assert response.data["student_card"] == "25011884"
        assert response.data["is_registered"] is False

    def test_lookup_by_personnel_number(
        self, api_client: APIClient, pre_registered_student: PreRegisteredStudent
    ) -> None:
        response = api_client.post(
            LOOKUP_URL,
            {"personnel_number": "1335090", "last_name": "Иванов"},
            format="json",
        )

        assert response.status_code == 200
        assert response.data["id"] == pre_registered_student.pk

    def test_lookup_by_snils_normalized(
        self, api_client: APIClient, pre_registered_student: PreRegisteredStudent
    ) -> None:
        response = api_client.post(
            LOOKUP_URL,
            {"snils": "184-573-628 06", "last_name": "Иванов"},
            format="json",
        )

        assert response.status_code == 200
        assert response.data["id"] == pre_registered_student.pk

    def test_lookup_not_found(self, api_client: APIClient) -> None:
        response = api_client.post(
            LOOKUP_URL,
            {"student_card": "00000000", "last_name": "Иванов"},
            format="json",
        )

        assert response.status_code == 404
        assert response.data["detail"] == "Предрегистрация не найдена"

    def test_lookup_requires_single_identifier(self, api_client: APIClient) -> None:
        response = api_client.post(
            LOOKUP_URL,
            {
                "student_card": "25011884",
                "snils": "18457362806",
                "last_name": "Иванов",
            },
            format="json",
        )

        assert response.status_code == 400

    def test_lookup_requires_last_name(
        self, api_client: APIClient, pre_registered_student: PreRegisteredStudent
    ) -> None:
        response = api_client.post(
            LOOKUP_URL, {"student_card": "25011884"}, format="json"
        )

        assert response.status_code == 400
        assert "last_name" in response.data

    def test_lookup_last_name_mismatch(
        self, api_client: APIClient, pre_registered_student: PreRegisteredStudent
    ) -> None:
        response = api_client.post(
            LOOKUP_URL,
            {"student_card": "25011884", "last_name": "Петров"},
            format="json",
        )

        assert response.status_code == 400
        assert "Фамилия не совпадает" in response.data["detail"]

    def test_lookup_last_name_case_insensitive(
        self, api_client: APIClient, pre_registered_student: PreRegisteredStudent
    ) -> None:
        response = api_client.post(
            LOOKUP_URL,
            {"student_card": "25011884", "last_name": "иванов"},
            format="json",
        )

        assert response.status_code == 200
        assert response.data["last_name"] == "Иванов"

    def test_lookup_ended_group_returns_404(
        self,
        api_client: APIClient,
        pre_registered_student: PreRegisteredStudent,
        study_group: StudyGroup,
    ) -> None:
        study_group.is_end = True
        study_group.save(update_fields=["is_end"])

        response = api_client.post(
            LOOKUP_URL,
            {"student_card": "25011884", "last_name": "Иванов"},
            format="json",
        )

        assert response.status_code == 404


@pytest.fixture
def pre_registered_mentor(departments) -> PreRegisteredStudent:
    return PreRegisteredStudent.objects.create(
        last_name="Ишханян",
        first_name="Маргарита",
        middle_name="Владимировна",
        personnel_number="1347607",
        role_id="mentor",
        department=departments["child"],
    )


@pytest.mark.django_db
class TestPreRegisteredMentorLookup:
    def test_lookup_by_personnel_number(
        self, api_client: APIClient, pre_registered_mentor: PreRegisteredStudent
    ) -> None:
        response = api_client.post(
            LOOKUP_URL,
            {"personnel_number": "1347607", "last_name": "Ишханян"},
            format="json",
        )

        assert response.status_code == 200
        assert response.data["id"] == pre_registered_mentor.pk
        assert response.data["role"] == "mentor"
        assert response.data["department_name"] == "Child Dept"
        assert response.data["group_name"] == ""
        assert response.data["student_card"] == ""
        assert response.data["is_registered"] is False

    def test_lookup_mentor_without_department(self, api_client: APIClient) -> None:
        PreRegisteredStudent.objects.create(
            last_name="Петров",
            first_name="Пётр",
            middle_name="",
            personnel_number="900099",
            role_id="mentor",
        )

        response = api_client.post(
            LOOKUP_URL,
            {"personnel_number": "900099", "last_name": "Петров"},
            format="json",
        )

        assert response.status_code == 200
        assert response.data["role"] == "mentor"
        assert response.data["department_name"] is None


@pytest.mark.django_db
class TestPreRegisteredStudentRegister:
    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
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
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == ["student@example.com"]
        assert "Вы успешно зарегистрированы" in mail.outbox[0].body

        pre_registered_student.refresh_from_db()
        assert pre_registered_student.user is not None
        assert (
            pre_registered_student.user.study_group_id
            == pre_registered_student.group_id
        )
        assert pre_registered_student.user.role.code == "student"

    def test_register_ended_group_returns_400(
        self,
        api_client: APIClient,
        pre_registered_student: PreRegisteredStudent,
        study_group: StudyGroup,
        roles: dict[str, Any],
    ) -> None:
        study_group.is_end = True
        study_group.save(update_fields=["is_end"])

        response = api_client.post(
            REGISTER_URL,
            {
                "id": pre_registered_student.pk,
                "email": "student@example.com",
                "password": "StrongPass123!",
            },
            format="json",
        )

        assert response.status_code == 400
        assert "завершила обучение" in response.data["detail"]

    def test_register_rolls_back_when_email_send_failed(
        self,
        api_client: APIClient,
        pre_registered_student: PreRegisteredStudent,
        roles: dict[str, Any],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        def _raise_send_mail(*args: Any, **kwargs: Any) -> None:
            raise RuntimeError("SMTP unavailable")

        monkeypatch.setattr(
            "accounts.services.preregistered_student_service.mail.send_mail",
            _raise_send_mail,
        )

        response = api_client.post(
            REGISTER_URL,
            {
                "id": pre_registered_student.pk,
                "email": "student@example.com",
                "password": "StrongPass123!",
            },
            format="json",
        )

        assert response.status_code == 500
        assert "Регистрация отменена" in response.data["detail"]

        pre_registered_student.refresh_from_db()
        assert pre_registered_student.user is None
        assert not get_user_model().objects.filter(email="student@example.com").exists()

    def test_register_already_registered(
        self,
        api_client: APIClient,
        pre_registered_student: PreRegisteredStudent,
        make_user,
        roles: dict[str, Any],
    ) -> None:
        pre_registered_student.user = make_user(
            role_code="user", email="existing@example.com"
        )
        pre_registered_student.save(update_fields=["user"])

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

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_register_mentor_creates_user_with_mentor_role(
        self,
        api_client: APIClient,
        pre_registered_mentor: PreRegisteredStudent,
        roles: dict[str, Any],
    ) -> None:
        response = api_client.post(
            REGISTER_URL,
            {
                "id": pre_registered_mentor.pk,
                "email": "mentor@example.com",
                "password": "StrongPass123!",
            },
            format="json",
        )

        assert response.status_code == 201
        assert response.data["user"]["email"] == "mentor@example.com"

        pre_registered_mentor.refresh_from_db()
        assert pre_registered_mentor.user is not None
        assert pre_registered_mentor.user.role.code == "mentor"
        assert (
            pre_registered_mentor.user.department_id
            == pre_registered_mentor.department_id
        )
        assert pre_registered_mentor.user.study_group_id is None

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_register_mentor_assigns_groups_from_project_teachers(
        self,
        api_client: APIClient,
        pre_registered_mentor: PreRegisteredStudent,
        study_group: StudyGroup,
        roles: dict[str, Any],
    ) -> None:
        semester = Semester.objects.create(
            code="26-27-1",
            name="Осень 26/27",
            position=1,
        )
        Settings.objects.update_or_create(
            code="active_semester_code",
            defaults={"description": "Active", "value": semester.code},
        )
        StudyGroupProjectTeacher.objects.create(
            semester=semester,
            study_group=study_group,
            mentor_full_name="Ишханян Маргарита Владимировна",
            external_teacher_id=pre_registered_mentor.personnel_number,
        )

        response = api_client.post(
            REGISTER_URL,
            {
                "id": pre_registered_mentor.pk,
                "email": "mentor-groups@example.com",
                "password": "StrongPass123!",
            },
            format="json",
        )

        assert response.status_code == 201
        pre_registered_mentor.refresh_from_db()
        mentor = pre_registered_mentor.user
        assert mentor is not None

        assignment = StudyGroupProjectTeacher.objects.get(
            study_group=study_group,
            semester=semester,
        )
        assert assignment.tutor_id == mentor.pk

        enrollment = StudyGroupSemester.objects.get(
            study_group=study_group,
            semester=semester,
        )
        assert list(enrollment.mentors.values_list("id", flat=True)) == [mentor.pk]

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
