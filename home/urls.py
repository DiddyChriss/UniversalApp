from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .views import *

app_name = 'home'
urlpatterns = [
    path('', base_view, name='home'),
    path('kontakt/', ContactView.as_view(), name='contact'),

]