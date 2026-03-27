
from django.contrib import admin
from django.urls import path,include
from core.views import home
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'), #it defines the core base home
    path('events/',include("events.urls")), ## it defines all tasks.url are included automatically
    path('users/', include('users.urls')),
]+ debug_toolbar_urls()


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)