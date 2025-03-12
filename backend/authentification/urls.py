# authentification/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView  # Importa estas vistas
from .views import RegisterView, CustomPasswordResetView, CustomPasswordResetConfirmView, UserProfileView, UserEditView, DeleteUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'authentification'  # Agrega esto para establecer un namespace


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    path('user-edit/', UserEditView.as_view(), name='user-edit'),
    path('delete_account/', DeleteUserView.as_view(), name='delete_account'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


