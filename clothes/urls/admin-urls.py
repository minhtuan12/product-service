from django.urls import path
from clothes import views

urlpatterns = [
    path('clothes-list', view = views.admin_get_clothes, name = 'clothes'),
    path('clothes', view = views.create, name = 'create-clothes'),
    path('clothes/<str:id>', view = views.update, name = 'update-clothes'),
    path('delete-clothes/<str:id>', view = views.delete, name = 'delete-clothes'),
]
