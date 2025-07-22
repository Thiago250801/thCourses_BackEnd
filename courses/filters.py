from django_filters import rest_framework as filters
from courses.models import Course

class CourseFilter(filters.FilterSet):
    # Gte = Greater than or equal to = maior ou igual a
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    # Lte = Less than or equal to = menor ou igual a
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    # Icontains = Contém
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    # Iexact = Igual a
    level = filters.CharFilter(field_name='level', lookup_expr='iexact')
    tags = filters.BaseInFilter(field_name='tags__name', lookup_expr='in')
    
    class Meta:
        model = Course
        fields = [ 'level', 'min_price', 'max_price', 'title', 'tags']