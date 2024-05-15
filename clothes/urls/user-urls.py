from django.urls import path
from clothes import views

urlpatterns = [
    path('clothes', view = views.clothes, name = 'clothes'),
]
