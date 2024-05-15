from django.urls import path, include

urlpatterns = [
    path('', include('book.urls.user-urls')),
    path('admin/', include('book.urls.admin-urls')),
    path('books/categories', include('book_categories.urls')),
]
