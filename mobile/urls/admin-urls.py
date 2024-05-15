from django.urls import path
from mobile import views

urlpatterns = [
    path('mobile-list', view = views.admin_get_mobile, name = 'mobile'),
    path('mobiles', view = views.create, name = 'create-mobile'),
    path('mobiles/<str:id>', view = views.update, name = 'update-mobile'),
    path('delete-mobile/<str:id>', view = views.delete, name = 'delete-mobile'),
]
