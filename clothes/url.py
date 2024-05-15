from django.urls import path, include

urlpatterns = [
    path('', include('clothes.urls.user-urls')),
    path('admin/', include('clothes.urls.admin-urls')),
    path('clothes/categories/', include('clothes_categories.urls')),
]
