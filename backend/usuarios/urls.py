from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, MeView, RoleViewSet, UserViewSet, UsuarioPdfViewSet

router = DefaultRouter()
router.register(r'auth/usuarios', UserViewSet, basename='auth-usuarios')
router.register(r'roles', RoleViewSet, basename='roles')
router.register(r'usuarios', UsuarioPdfViewSet, basename='usuarios')

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='auth_login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth_refresh'),
    path('auth/me/', MeView.as_view(), name='auth_me'),
    path('', include(router.urls)),
]
