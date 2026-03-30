from django.shortcuts import render
from django.views.generic import TemplateView
from events.models import Event,Category
# Create your views here.
def home(request):
    events = Event.objects.select_related('category').prefetch_related('participants')[:20]
    categories = Category.objects.all()
    return render(request,'core/home.html',{"events":events,"categories":categories})

# New Class-Based Views for static pages


class GalleryView(TemplateView):
    template_name = 'core/gallery.html'

class ScheduleView(TemplateView):
    template_name = 'core/schedule.html'

class ContactView(TemplateView):
    template_name = 'core/contact.html'

class SpeakerListView(TemplateView):
    template_name='core/speakers.html'