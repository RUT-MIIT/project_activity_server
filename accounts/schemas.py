from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

login_schema = swagger_auto_schema(
    operation_description="Получение JWT токена по email и паролю",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email", "password"],
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, example="user@example.com"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, example="your_password"
            ),
        },
    ),
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(
                    type=openapi.TYPE_STRING, example="<refresh_token>"
                ),
                "access": openapi.Schema(
                    type=openapi.TYPE_STRING, example="<access_token>"
                ),
            },
        ),
        401: "Неверные учетные данные",
    },
)
