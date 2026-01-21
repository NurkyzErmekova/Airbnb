from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, LoginView, LogoutView,
    PropertyViewSet, BookingViewSet,
    CityListView, ReviewCreateView,
)

router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='properties')
router.register(r'bookings', BookingViewSet, basename='bookings')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cities/', CityListView.as_view(), name='city-list'),
    path('reviews/create/', ReviewCreateView.as_view(), name='review-create'),
]