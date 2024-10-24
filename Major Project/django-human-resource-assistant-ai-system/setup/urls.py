""" Global url project """

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pessoal/', include('apps.personal.urls')),
    path('empresarial/', include('apps.business.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('', include('apps.general.urls')),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)