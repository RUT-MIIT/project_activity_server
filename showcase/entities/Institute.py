from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny
from showcase.models import Institute


class InstituteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для институтов/академий.
    """
    class Meta:
        model = Institute
        fields = [
            'code',
            'name',
        ]


class InstituteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet только для чтения институтов/академий.
    Доступен для всех пользователей.
    """
    queryset = Institute.objects.filter(is_active=True)
    serializer_class = InstituteSerializer
    permission_classes = [AllowAny]
    lookup_field = 'code'



