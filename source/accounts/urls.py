from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import login_view, logout_view, RegistrationView, ProfileView, UserChangeView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('<int:pk>/profile/', ProfileView.as_view(), name='profile'),
    path('<int:pk>/profile/edit/', UserChangeView.as_view(), name='profile_change'),

]