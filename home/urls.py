from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .views import *

app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('kontakt/', ContactView.as_view(), name='contact'),
    path('onas/', AboutView.as_view(), name='about'),
    path('pres/', PresView.as_view(), name='pres'),
    path('zaplac/', PayView.as_view(), name='pay'),

]