from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.FinanceProfileView.as_view()),
    path("transactions/", views.TransactionsView.as_view()),
    path("transaction/", views.TransactionView.as_view()),
    path("transaction/<int:id>/", views.GetTransactionView.as_view()),
]
