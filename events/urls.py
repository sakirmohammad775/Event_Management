from django.urls import path
from events.views import dashboard,event_create,event_list

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    
    #event
    path('event_list/',event_list,name='event_list'),
    path('create/', event_create, name='event_create'),
]
