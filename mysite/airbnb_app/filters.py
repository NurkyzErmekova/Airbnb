from django_filters import rest_framework as filters
from .models import Property

class PropertyFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price_per_night", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price_per_night", lookup_expr='lte')
    city_id = filters.NumberFilter(field_name="city__id")

    class Meta:
        model = Property
        fields = ['city_id', 'property_type', 'max_guests', 'min_price', 'max_price']