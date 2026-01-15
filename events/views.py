from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from events.models import Event, Category, Participant
from events.forms import EventForm, CategoryForm, ParticipantForm
from django.utils import timezone

def organizer_dashboard(request):
    today = timezone.localdate()

    events = (
        Event.objects
        .select_related('category')
        .prefetch_related('participants')
    )

    filter_type = request.GET.get('filter')

    if filter_type == 'upcoming':
        filtered_events = events.filter(date__gt=today)
    elif filter_type == 'past':
        filtered_events = events.filter(date__lt=today)
    else:
        filtered_events = events

    
    # ===== SEARCH =====
    search_query = request.GET.get('q')
    if search_query:
        filtered_events = filtered_events.filter(
            name__icontains=search_query
        ) | filtered_events.filter(
            location__icontains=search_query
        )
        
    context = {
        'total_events': events.count(),
        'upcoming_events': events.filter(date__gt=today).count(),
        'past_events': events.filter(date__lt=today).count(),
        'total_participants': Participant.objects.count(),
        'todays_events': events.filter(date=today),
        'filtered_events': filtered_events,
        'filter_type': filter_type,
    }

    return render(request, 'dashboard/organizer_dashboard.html', context)


# --------- Category ----------#

def category_list(request):
    categories = Category.objects.all()
    return render(request, "category_list.html", {"categories": categories})


def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("category_list")
    return render(request, "form.html", {"form": form})


def category_update(request, pk):
    # category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("category_list")
    return render(request, "form.html", {"form": form})


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect("category_list")
    return render(request, "confirm_delete.html")


# --------- Event Crud --------#


def event_list(request):
    events = Event.objects.select_related("category")
    return render(request, "event_list.html", {"events": events})


def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("event_list")
    return render(request, "form.html", {"form": form})


def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)  # get the event

    form = EventForm(request.POST or None, instance=event)
    # instance=event → pre-fills form with existing data
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, 'form.html', {
        'form': form,
        'event': event
    })


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "POST":
        event.delete()
        return redirect('event_list')

    return render(request, 'confirm_delete.html', {
        'event': event
    })

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event_detail.html', {'event': event})

#-----------Participant CRUD------#


def participant_list(request):
    participants = Participant.objects.prefetch_related('events')
    return render(request, 'participants/participants_list.html', {'participants': participants})

def participant_create(request):
    form = ParticipantForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('participant_list')
    return render(request,'form.html', {'form': form})

def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    form = ParticipantForm(request.POST or None, instance=participant)
    if form.is_valid():
        form.save()
        return redirect('participant_list')
    return render(request, 'form.html', {'form': form})

def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant_list')
    return render(request, 'confirm_delete.html')