from django.urls import path
from book import views

urlpatterns = [
    path('books', view = views.books, name = 'books'),
]
