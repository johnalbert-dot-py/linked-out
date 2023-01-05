from django.urls import path
from .views import Login, Logout
from .views import register


urlpatterns = [
    path("", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("register/", register, name="register"),
]
