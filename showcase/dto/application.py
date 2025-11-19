"""DTO для работы с проектными заявками."""

from typing import Any, Optional


def serialize_comment_author(author) -> dict:
    """Сериализует автора комментария с role и department.

    Args:
        author: User объект

    Returns:
        dict: Сериализованные данные автора

    """
    if not author:
        return {"id": None, "name": None, "role_name": None, "department_name": None}

    initials = []
    if author.first_name:
        initials.append(f"{author.first_name[0]}.")
    middle_value = getattr(author, "middle_name", None)
    if middle_value:
        initials.append(f"{middle_value[0]}.")
    initials_part = " ".join(initials).strip()
    if author.last_name and initials_part:
        short_name = f"{author.last_name} {initials_part}"
    elif author.last_name:
        short_name = author.last_name
    else:
        short_name = initials_part or None
    return {
        "id": author.id,
        "name": (
            f"{author.first_name} {author.last_name}".strip()
            if author.first_name and author.last_name
            else None
        ),
        "short_name": short_name,
        "role_name": (
            author.role.name if hasattr(author, "role") and author.role else None
        ),
        "department_name": (
            author.department.name
            if hasattr(author, "department") and author.department
            else None
        ),
    }


class ProjectApplicationCreateDTO:
    """DTO для создания заявки - только данные, никакой логики"""

    def __init__(
        self,
        company: str,
        title: Optional[str] = None,
        author_lastname: Optional[str] = None,
        author_firstname: Optional[str] = None,
        author_email: Optional[str] = None,
        author_phone: Optional[str] = None,
        problem_holder: Optional[str] = None,
        goal: Optional[str] = None,
        barrier: Optional[str] = None,
        author_middlename: Optional[str] = None,
        author_role: Optional[str] = None,
        author_division: Optional[str] = None,
        company_contacts: str = "",
        target_institutes: Optional[list[str]] = None,
        project_level: str = "",
        existing_solutions: str = "",
        context: Optional[str] = None,
        stakeholders: Optional[str] = None,
        recommended_tools: Optional[str] = None,
        experts: Optional[str] = None,
        additional_materials: Optional[str] = None,
        needs_consultation: bool = False,
        description: Optional[str] = None,  # Для совместимости с тестами
        **kwargs,
    ):
        self.title = title or ""
        self.company = company
        self.description = description  # Сохраняем для совместимости
        self.author_lastname = author_lastname
        self.author_firstname = author_firstname
        self.author_middlename = author_middlename
        self.author_email = author_email
        self.author_phone = author_phone
        self.author_role = author_role
        self.author_division = author_division
        self.company_contacts = company_contacts
        self.target_institutes = target_institutes or []
        self.project_level = project_level
        self.problem_holder = problem_holder
        self.goal = goal
        self.barrier = barrier
        self.existing_solutions = existing_solutions
        self.context = context
        self.stakeholders = stakeholders
        self.recommended_tools = recommended_tools
        self.experts = experts
        self.additional_materials = additional_materials
        self.needs_consultation = needs_consultation

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProjectApplicationCreateDTO":
        """Создание из словаря"""
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        """Преобразование в словарь"""
        return {
            "title": self.title,
            "description": self.description,
            "company": self.company,
            "author_lastname": self.author_lastname,
            "author_firstname": self.author_firstname,
            "author_middlename": self.author_middlename,
            "author_email": self.author_email,
            "author_phone": self.author_phone,
            "author_role": self.author_role,
            "author_division": self.author_division,
            "company_contacts": self.company_contacts,
            "target_institutes": self.target_institutes,
            "project_level": self.project_level,
            "problem_holder": self.problem_holder,
            "goal": self.goal,
            "barrier": self.barrier,
            "existing_solutions": self.existing_solutions,
            "context": self.context,
            "stakeholders": self.stakeholders,
            "recommended_tools": self.recommended_tools,
            "experts": self.experts,
            "additional_materials": self.additional_materials,
            "needs_consultation": self.needs_consultation,
        }


class ProjectApplicationUpdateDTO:
    """DTO для обновления заявки - только изменяемые поля"""

    def __init__(
        self,
        title: Optional[str] = None,
        company: Optional[str] = None,
        author_lastname: Optional[str] = None,
        author_firstname: Optional[str] = None,
        author_middlename: Optional[str] = None,
        author_email: Optional[str] = None,
        author_phone: Optional[str] = None,
        author_role: Optional[str] = None,
        author_division: Optional[str] = None,
        company_contacts: Optional[str] = None,
        target_institutes: Optional[list[str]] = None,
        project_level: Optional[str] = None,
        problem_holder: Optional[str] = None,
        goal: Optional[str] = None,
        barrier: Optional[str] = None,
        existing_solutions: Optional[str] = None,
        context: Optional[str] = None,
        stakeholders: Optional[str] = None,
        recommended_tools: Optional[str] = None,
        experts: Optional[str] = None,
        additional_materials: Optional[str] = None,
        needs_consultation: Optional[bool] = None,
        **kwargs,
    ):
        self.title = title
        self.company = company
        self.author_lastname = author_lastname
        self.author_firstname = author_firstname
        self.author_middlename = author_middlename
        self.author_email = author_email
        self.author_phone = author_phone
        self.author_role = author_role
        self.author_division = author_division
        self.company_contacts = company_contacts
        self.target_institutes = target_institutes
        self.project_level = project_level
        self.problem_holder = problem_holder
        self.goal = goal
        self.barrier = barrier
        self.existing_solutions = existing_solutions
        self.context = context
        self.stakeholders = stakeholders
        self.recommended_tools = recommended_tools
        self.experts = experts
        self.additional_materials = additional_materials
        self.needs_consultation = needs_consultation

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProjectApplicationUpdateDTO":
        """Создание из словаря"""
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        """Преобразование в словарь, исключая None значения"""
        result = {}
        for key, value in self.__dict__.items():
            if value is not None:
                result[key] = value
        return result


class ProjectApplicationReadDTO:
    """DTO для чтения заявки - оптимизированный набор полей"""

    def __init__(self, application):
        self.id = application.id
        self.title = application.title
        self.company = application.company
        self.creation_date = application.creation_date
        self.needs_consultation = application.needs_consultation

        # Нумерация заявок
        self.application_year = application.application_year
        self.year_sequence_number = application.year_sequence_number
        self.print_number = application.print_number

        # Статус
        self.status = (
            {"code": application.status.code, "name": application.status.name}
            if application.status
            else None
        )

        # Автор
        self.author = (
            {
                "id": application.author.id if application.author else None,
                "name": f"{application.author_lastname} {application.author_firstname}",
                "email": application.author_email,
                "phone": application.author_phone,
                "role": application.author_role,
                "division": application.author_division,
            }
            if application.author
            else None
        )

        # Контактные данные
        self.author_lastname = application.author_lastname
        self.author_firstname = application.author_firstname
        self.author_middlename = application.author_middlename
        self.author_email = application.author_email
        self.author_phone = application.author_phone
        self.author_role = application.author_role
        self.author_division = application.author_division

        # О проекте
        self.company_contacts = application.company_contacts
        self.project_level = application.project_level

        # Проблема
        self.problem_holder = application.problem_holder
        self.goal = application.goal
        self.barrier = application.barrier
        self.existing_solutions = application.existing_solutions

        # Контекст
        self.context = application.context
        self.stakeholders = application.stakeholders
        self.recommended_tools = application.recommended_tools
        self.experts = application.experts
        self.additional_materials = application.additional_materials

        # Связанные объекты
        self.target_institutes = [
            {"code": inst.code, "name": inst.name}
            for inst in application.target_institutes.all()
        ]

        self.involved_users = [
            {
                "id": involved.id,
                "user": {
                    "id": involved.user.id,
                    "name": involved.user.get_full_name(),
                    "email": involved.user.email,
                },
                "added_at": involved.added_at,
                "added_by": (
                    {
                        "id": involved.added_by.id,
                        "name": involved.added_by.get_full_name(),
                    }
                    if involved.added_by
                    else None
                ),
            }
            for involved in application.involved_users.all()
        ]

        self.involved_departments = [
            {
                "id": involved.id,
                "department": {
                    "id": involved.department.id,
                    "name": involved.department.name,
                    "short_name": involved.department.short_name,
                },
                "added_at": involved.added_at,
                "added_by": (
                    {
                        "id": involved.added_by.id,
                        "name": involved.added_by.get_full_name(),
                    }
                    if involved.added_by
                    else None
                ),
            }
            for involved in application.involved_departments.all()
        ]

        # Получаем комментарии напрямую из заявки
        try:
            comments = (
                application.comments.all()
                .select_related("author", "author__role", "author__department")
                .order_by("-created_at")
            )
            self.comments = [
                {
                    "id": comment.id,
                    "field": comment.field,
                    "text": comment.text,
                    "author": serialize_comment_author(comment.author),
                    "created_at": (
                        comment.created_at.isoformat() if comment.created_at else None
                    ),
                }
                for comment in comments
            ]
        except Exception:
            self.comments = []

    def to_dict(self) -> dict[str, Any]:
        """Преобразование в словарь для JSON"""
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "creation_date": self.creation_date.isoformat(),
            "needs_consultation": self.needs_consultation,
            "application_year": self.application_year,
            "year_sequence_number": self.year_sequence_number,
            "print_number": self.print_number,
            "status": self.status,
            "author": self.author,
            "author_lastname": self.author_lastname,
            "author_firstname": self.author_firstname,
            "author_middlename": self.author_middlename,
            "author_email": self.author_email,
            "author_phone": self.author_phone,
            "author_role": self.author_role,
            "author_division": self.author_division,
            "company_contacts": self.company_contacts,
            "project_level": self.project_level,
            "problem_holder": self.problem_holder,
            "goal": self.goal,
            "barrier": self.barrier,
            "existing_solutions": self.existing_solutions,
            "context": self.context,
            "stakeholders": self.stakeholders,
            "recommended_tools": self.recommended_tools,
            "experts": self.experts,
            "additional_materials": self.additional_materials,
            "target_institutes": self.target_institutes,
            "involved_users": self.involved_users,
            "involved_departments": self.involved_departments,
            "comments": self.comments,
        }


class ProjectApplicationListDTO:
    """DTO для списка заявок - минимальный набор полей"""

    def __init__(self, application):
        self.id = application.id
        self.title = application.title
        self.company = application.company
        self.creation_date = application.creation_date
        self.needs_consultation = application.needs_consultation
        # Количество комментариев: используем аннотацию, если есть, иначе fallback к count()
        annotated_count = getattr(application, "comments_count", None)
        self.comments_count = (
            int(annotated_count)
            if annotated_count is not None
            else application.comments.count()
        )

        # Нумерация заявок
        self.application_year = application.application_year
        self.year_sequence_number = application.year_sequence_number
        self.print_number = application.print_number

        # Статус
        self.status = (
            {"code": application.status.code, "name": application.status.name}
            if application.status
            else None
        )

        # Автор (только имя)
        self.author_name = (
            f"{application.author_lastname} {application.author_firstname}"
        )
        self.author_email = application.author_email

    def to_dict(self) -> dict[str, Any]:
        """Преобразование в словарь для JSON"""
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "creation_date": self.creation_date.isoformat(),
            "needs_consultation": self.needs_consultation,
            "application_year": self.application_year,
            "year_sequence_number": self.year_sequence_number,
            "print_number": self.print_number,
            "status": self.status,
            "author_name": self.author_name,
            "author_email": self.author_email,
            "comments_count": self.comments_count,
        }
