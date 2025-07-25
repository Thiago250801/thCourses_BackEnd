from rest_framework import viewsets, decorators
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request

from courses.filters import CourseFilter
from courses.models import Course, Enrollment
from courses.serializers import CourseSerializer, ReviewSerializer


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    # Ordernando os cursos do mais recente para o mais antigo
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]  # Permite acesso a todos os usuários
    filterset_class = CourseFilter # /courses/?min_price=100
    ordering_fields = ['created_at', 'price'] # /courses/?ordering=created_at ou /courses/?ordering=price
    
    @decorators.action(detail=True, methods=['get'])
    def reviews(self, request: Request, pk=None):
        """
        Custom action to retrieve reviews for a specific course.
        """
        course = self.get_object()
        reviews = course.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    # Defined the enrolment date for the course if the user is authenticated
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        enrolled_at = None
        if request.user.is_authenticated:
            enrolled = Enrollment.objects.filter(
                user=request.user,
                course=instance
            ).first()
            if enrolled:
                enrolled_at = enrolled.enrolled_at
                
        return Response({
            **serializer.data,
            'enrolled_at': enrolled_at
        })