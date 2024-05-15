from django.urls import path, include

urlpatterns = [
    path('', include('mobile.urls.user-urls')),
    path('admin/', include('mobile.urls.admin-urls')),
    path('mobiles/categories', include('mobile_categories.urls')),
]
