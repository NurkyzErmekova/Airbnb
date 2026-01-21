from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="Airbnb API",
        default_version='v1',
        description="API для бронирования жилья",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('airbnb_app.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
