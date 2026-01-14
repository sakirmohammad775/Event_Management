from django.urls import path
from events.views import event_create,event_list,category_list,category_create,category_delete,category_update,participant_create,participant_list,participant_delete,participant_update,event_delete,event_update,organizer_dashboard

urlpatterns = [
    path('dashboard/organizer/', organizer_dashboard, name='organizer_dashboard'),


    # path('user-dashboard/',user_dashboard),
    
    #------------- Event ------------
    path('event_list/',event_list,name='event_list'),
    path('create/', event_create, name='event_create'),
    path('<int:pk>/update/', event_update, name='event_update'),
    path('<int:pk>/delete/', event_delete, name='event_delete'),
    
    # ----------- CATEGORY ----------
    path('categories/',category_list, name='category_list'),
    path('categories/create/',category_create, name='category_create'),
    path('categories/<int:pk>/update/',category_update, name='category_update'),
    path('categories/<int:pk>/delete/',category_delete, name='category_delete'),

    # ---------- PARTICIPANT ----------
    path('participants/', participant_list, name='participant_list'),
    path('participants/create/', participant_create, name='participant_create'),
    path('participants/<int:pk>/update/', participant_update, name='participant_update'),
    path('participants/<int:pk>/delete/', participant_delete, name='participant_delete'),
]
