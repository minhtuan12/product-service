from django.urls import path
from book_categories import views

urlpatterns = [
    path('', views.get_all_categories),
]
