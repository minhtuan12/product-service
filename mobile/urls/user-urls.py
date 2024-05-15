from django.urls import path
from mobile import views

urlpatterns = [
    path('mobiles', view = views.mobiles, name = 'mobile'),
]
