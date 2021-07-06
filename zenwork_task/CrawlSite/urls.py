from django.urls import path
from django.urls.conf import include
from . import views


app_name = 'crawlsites'
urlpatterns = [
    path('user_records/',views.get_records, name="user_records"),
    path('signupview/',views.signupview, name="signupview"),
    path('signup/',views.signup, name="signup"),
    path('loginview/',views.loginview, name="loginview"),
    path('login/',views.login, name="login"),
    path('profile/',views.profile, name="profile")
]