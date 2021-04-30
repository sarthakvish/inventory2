from django.contrib import admin
from django.urls import path,include,re_path
from inventory_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory_app.urls')),
    path('performance/', include(('datascience.urls', 'datascience'))),
    path('accounts/', include('allauth.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
# urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# urlpatterns+= static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)