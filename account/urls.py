from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("", views.GetUserData.as_view(), name = "user_data"),
    path("forgot-password/", views.ForgorPassword.as_view(), name = "forgot_password"),
    path("register/", views.Register.as_view(), name = "register"),
]