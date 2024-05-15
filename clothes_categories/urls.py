from django.urls import path
from clothes_categories import views

urlpatterns = [
    path('', views.get_all_categories),
]
