from django.urls import path
from mobile_categories import views

urlpatterns = [
    path('', views.get_all_categories),
]
