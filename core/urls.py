from django.urls import path
from core.views import home,SpeakerListView,GalleryView,ContactView,ScheduleView

urlpatterns = [
    path('', home, name='home'),
    path('speakers/', SpeakerListView.as_view(), name='speakers'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('schedule/', ScheduleView.as_view(), name='schedule'),
    path('contact/', ContactView.as_view(), name='contact'),
]
