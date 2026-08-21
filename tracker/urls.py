from django.urls import path
from . import views

urlpatterns = [
    path('assets/', views.get_all_assets),
    path('checkouts', views.checkouts),
    path('checkouts/<int:pk>/approve', views.approve_checkout),
    path('checkouts/<int:pk>/reject', views.reject_checkout),
    path('checkouts/user/<int:pk>', views.user_checkouts),
]