from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet, UserViewSet, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    
    
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    
    
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
