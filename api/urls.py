
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('galeria.urls')),
    path('adicionar/', include('galeria.urls')),
    path('login/', include('galeria.urls')),
    path('cadastro/', include('galeria.urls')),
    path('logout/', include('galeria.urls')),
    path('colecoes/', include('galeria.urls')),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)