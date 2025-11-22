from django.urls import path
from .views import (
    signup_view, login_view, logout_view, dashboard,
    list_transactions,add_transaction, edit_transaction, delete_transaction
)

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),



    path('', list_transactions, name='list_transactions'),
    path('add/', add_transaction, name='add_transaction'),
    path('edit/<int:pk>/',edit_transaction, name='edit_transaction'),
    path('edit/<int:pk>/',edit_transaction, name='edit_transaction'),  # 👈 NEW
    path('delete/<int:pk>/',delete_transaction, name='delete_transaction'),  # 👈 NEW
]
