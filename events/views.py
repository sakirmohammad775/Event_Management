from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from events.models import Event,Category,Participant
from events.forms import EventForm,CategoryForm,ParticipantForm


# Create your views here.
def home(request):
    return HttpResponse('welcome to the')

def contact(request):
    return HttpResponse('welcome to the contact page')

def dashboard(request):
    return render(request, 'dashboard.html')

#-----Event Crud-----#

def event_list(request):
    events=Event.objects.select_related('category')
    return render(request,'event_list.html',{'events':events})

def event_create(request):
    form =EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request,'form.html',{'form':form})

def event_update(request):
    form=EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request,'event_list.html',{'form':form})

def event_delete(request):
    event=get_object_or_404(Event,pk=pk)
    if request.method=='POST':
        event.delete()
        return redirect('event_list')
    return render(request,'confirm_delete.html')