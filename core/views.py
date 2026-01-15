from django.shortcuts import render
from events.models import Event
# Create your views here.
def home(request):
    events = Event.objects.select_related('category').prefetch_related('participants')[:20]
    return render(request,'core/home.html',{"events":events})