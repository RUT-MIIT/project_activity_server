"""Тесты GET /api/accounts/user/ для роли student."""

from __future__ import annotations

from typing import Any

import pytest
from rest_framework.test import APIClient

from accounts.models import PreRegisteredStudent
from showcase.models import Institute
from teams.models import Direction, StudyGroup

USER_ME_URL = "/api/accounts/user/"


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
        profile="Организация бизнес-процессов",
        form="Очная",
        direction=direction,
        institute=institute,
    )


@pytest.fixture
def student_user(
    make_user,
    study_group: StudyGroup,
) -> Any:
    user = make_user(role_code="student", email="student@example.com")
    user.study_group = study_group
    user.middle_name = "Иванович"
    user.save(update_fields=["study_group", "middle_name"])
    PreRegisteredStudent.objects.create(
        last_name=user.last_name,
        first_name=user.first_name,
        middle_name=user.middle_name,
        student_card="25011884",
        snils="18457362806",
        personnel_number="1335090",
        group=study_group,
        user=user,
    )
    return user


@pytest.mark.django_db
class TestUserMeStudent:
    def test_user_me_returns_full_student_info(
        self,
        api_client: APIClient,
        student_user: Any,
        study_group: StudyGroup,
    ) -> None:
        api_client.force_authenticate(user=student_user)

        response = api_client.get(USER_ME_URL)

        assert response.status_code == 200
        assert response.data["email"] == "student@example.com"
        assert response.data["role"] == "student"
        assert response.data["student_card"] == "25011884"
        assert response.data["personnel_number"] == "1335090"
        assert response.data["snils"] == "18457362806"
        assert response.data["institute_code"] == "AGA"

        group_data = response.data["study_group"]
        assert group_data["id"] == study_group.id
        assert group_data["name"] == "АМБ-211"
        assert group_data["code"] == "АМБ-2025-11"
        assert group_data["enrollment_year"] == 2025
        assert group_data["course_number"] == 2
        assert group_data["profile"] == "Организация бизнес-процессов"
        assert group_data["form"] == "Очная"
        assert group_data["direction"]["code"] == "25.03.03"
        assert group_data["institute"]["code"] == "AGA"

    def test_user_me_non_student_has_null_student_fields(
        self,
        api_client: APIClient,
        make_user,
    ) -> None:
        user = make_user(role_code="user", email="regular@example.com")
        api_client.force_authenticate(user=user)

        response = api_client.get(USER_ME_URL)

        assert response.status_code == 200
        assert response.data["role"] == "user"
        assert response.data["study_group"] is None
        assert response.data["student_card"] is None
        assert response.data["personnel_number"] is None
        assert response.data["snils"] is None
