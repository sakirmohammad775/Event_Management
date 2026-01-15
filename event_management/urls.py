
from django.contrib import admin
from django.urls import path,include
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'), #it defines the core base home
    
    path('events/',include("events.urls")) ## it defines all tasks.url are included automatically
]
