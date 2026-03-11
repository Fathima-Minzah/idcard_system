from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from two_factor.urls import urlpatterns as tf_urls

from employees.views import TwoFactorLoginView
from employees.custom_admin import staff_admin_site


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('admin/', staff_admin_site.urls),
    path('', include('employees.urls')),          # Your app URLs
    path('', include(tf_urls)),

    #path('account/login/', TwoFactorLoginView.as_view(), name='login'),
    #path('account/', include(tf_urls)), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)