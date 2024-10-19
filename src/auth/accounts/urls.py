from django.urls import path
from .views import RegisterView, MyTokenObtainPairView, get_account_info, delete_account, update_account
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('info', get_account_info, name='get_user_info'),
    path('delete', delete_account, name='delete_account'),
    path('update', update_account, name='update_account')
]