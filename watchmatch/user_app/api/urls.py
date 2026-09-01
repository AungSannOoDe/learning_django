from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import registration_view,logout_view,profile_view,login_view
urlpatterns=[
    path("register",registration_view,name="register"),
    path("logout",logout_view,name="logout"),
    path("profile/", profile_view, name="profile"),
    path("login",login_view,name="login")
]