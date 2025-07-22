from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from courses.filters import CourseFilter
from courses.models import Course
from courses.serializers import CourseSerializer


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    # Ordernando os cursos do mais recente para o mais antigo
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]  # Permite acesso a todos os usuários
    filterset_class = CourseFilter # /courses/?min_price=100
    ordering_fields = ['created_at', 'price'] # /courses/?ordering=created_at ou /courses/?ordering=price