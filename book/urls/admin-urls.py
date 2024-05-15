from django.urls import path
from book import views

urlpatterns = [
    path('book-list', view = views.admin_get_books, name = 'books'),
    path('books', view = views.create, name = 'create-book'),
    path('books/<str:id>', view = views.update, name = 'update-book'),
    path('delete-book/<str:id>', view = views.delete, name = 'delete-book'),
]
