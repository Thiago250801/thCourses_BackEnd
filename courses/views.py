from rest_framework import viewsets, decorators, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import APIException, ValidationError
from courses.filters import CourseFilter
from courses.models import Course, Enrollment
from courses.serializers import CourseSerializer, ReviewSerializer

from django.db.models import Avg, Count


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    # Ordernando os cursos do mais recente para o mais antigo
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]  # Permite acesso a todos os usuários
    filterset_class = CourseFilter  # /courses/?min_price=100
    # /courses/?ordering=created_at ou /courses/?ordering=price
    ordering_fields = ['created_at', 'price']

    @decorators.action(detail=True, methods=['get'])
    def reviews(self, request: Request, pk=None):
        """
        Custom action to retrieve reviews for a specific course.
        """
        course = self.get_object()
        reviews = course.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @decorators.action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def submit_review(self, request: Request, pk=None):
        """
        Custom action to submit a review for a specific course.
        Requires authentication.
        """
        course = self.get_object()
        user = request.user

        if not Enrollment.objects.filter(user=user, course=course).exists():
            raise APIException(
                "Você precisa estar matriculado neste curso para enviar uma avaliação.")

        if course.reviews.filter(user=user).exists():
            raise APIException("Você já enviou uma avaliação para este curso.")
        data = {
            "rating": request.data.get('rating'),
            "comment": request.data.get('comment'),
        }
        serializer = ReviewSerializer(data=data)
        if not serializer.is_valid():
            raise ValidationError(format_serializer_error(serializer.errors))

        serializer.save(user=user, course=course)

        aggregate = course.reviews.aggregate(
            average_rating=Avg('rating'),
            total_reviews=Count('id')
        )
        
        course.average_rating = aggregate['average_rating'] or 0
        course.total_reviews = aggregate['total_reviews'] or 0
        course.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
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
