from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_transactions, name='list_transactions'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('edit/<int:pk>/', views.edit_transaction, name='edit_transaction'),
    path('edit/<int:pk>/', views.edit_transaction, name='edit_transaction'),  # 👈 NEW
    path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),  # 👈 NEW
]
