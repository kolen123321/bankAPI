from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.AuthView.as_view()),
    path("register/", views.RegisterView.as_view()),
    path("verificate/<int:id>/", views.VerificateUserView.as_view())
]
