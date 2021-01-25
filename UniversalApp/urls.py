
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('', include('eshop.urls', namespace='shop')),
    path('sklep/', include('eshop.api.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('sklep/logowanie/resethasla/wyslane/',
         auth_views.PasswordResetDoneView.as_view(
                                                  template_name="shop/login/shop_reset_password_send.html"),
                                                  name='password_reset_done'
        ),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
                                                     template_name="shop/login/shop_reset_password_confirm.html"),
                                                     name='password_reset_confirm'
        ),
    path('sklep/logowanie/resethasla/zaloguj/',
         auth_views.PasswordResetCompleteView.as_view(
                                                      template_name="shop/login/shop_reset_password_done.html"),
                                                      name='password_reset_complete'
        ),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)