from django.urls import path
from views import *
from django.urls import reverse

urlpatterns = [
    path('', home, name='home'),
    path('coffee/', coffee, name='coffee'),
]