from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
)
from django.contrib.auth.models import Group
from events.models import Event, Category
from events.forms import EventForm, CategoryForm


# ─────────────────────────────────────────────
#  Reusable Mixins
# ─────────────────────────────────────────────

class OrganizerRequiredMixin(UserPassesTestMixin):
    """Allow only users in the Organizer group."""
    login_url = "no-permission"

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.groups.filter(name="Organizer").exists()
        )


class ParticipantRequiredMixin(UserPassesTestMixin):
    """Allow only users in the Participant group."""
    login_url = "no-permission"

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.groups.filter(name="Participant").exists()
        )


# ─────────────────────────────────────────────
#  Organizer Dashboard
# ─────────────────────────────────────────────

class OrganizerDashboardView(LoginRequiredMixin, OrganizerRequiredMixin, TemplateView):
    template_name = "dashboard/organizer_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()

        events = Event.objects.select_related("category").prefetch_related("participants")

        filter_type = self.request.GET.get("filter")
        if filter_type == "upcoming":
            filtered_events = events.filter(date__gt=today)
        elif filter_type == "past":
            filtered_events = events.filter(date__lt=today)
        else:
            filtered_events = events

        search_query = self.request.GET.get("q")
        if search_query:
            filtered_events = (
                filtered_events.filter(name__icontains=search_query)
                | filtered_events.filter(location__icontains=search_query)
            )

        try:
            participant_group = Group.objects.get(name="Participant")
            total_participants = participant_group.user_set.count()
        except Group.DoesNotExist:
            total_participants = 0

        context.update({
            "total_events": events.count(),
            "upcoming_events": events.filter(date__gt=today).count(),
            "past_events": events.filter(date__lt=today).count(),
            "total_participants": total_participants,
            "todays_events": events.filter(date=today),
            "filtered_events": filtered_events,
            "filter_type": filter_type,
        })
        return context


# ─────────────────────────────────────────────
#  Participant Dashboard
# ─────────────────────────────────────────────

class ParticipantDashboardView(LoginRequiredMixin, ParticipantRequiredMixin, TemplateView):
    template_name = "dashboard/participant_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rsvp_events"] = (
            self.request.user.rsvp_events
            .select_related("category")
            .order_by("date")
        )
        return context


# ─────────────────────────────────────────────
#  Category CRUD
# ─────────────────────────────────────────────

class CategoryListView(ListView):
    model = Category
    template_name = "events/category_list.html"
    context_object_name = "categories"


class CategoryCreateView(LoginRequiredMixin, OrganizerRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "events/form.html"
    success_url = reverse_lazy("category_list")


class CategoryUpdateView(LoginRequiredMixin, OrganizerRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "events/form.html"
    success_url = reverse_lazy("category_list")


class CategoryDeleteView(LoginRequiredMixin, OrganizerRequiredMixin, DeleteView):
    model = Category
    template_name = "events/confirm_delete.html"
    success_url = reverse_lazy("category_list")


# ─────────────────────────────────────────────
#  Event CRUD
# ─────────────────────────────────────────────

class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"
    queryset = Event.objects.select_related("category")


class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Tell the template if the current user has already RSVP'd
        if self.request.user.is_authenticated:
            context["user_has_rsvp"] = self.object.participants.filter(
                pk=self.request.user.pk
            ).exists()
        else:
            context["user_has_rsvp"] = False
        return context


class EventCreateView(LoginRequiredMixin, OrganizerRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "events/form.html"
    success_url = reverse_lazy("event_list")


class EventUpdateView(LoginRequiredMixin, OrganizerRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "events/form.html"
    success_url = reverse_lazy("event_list")


class EventDeleteView(LoginRequiredMixin, OrganizerRequiredMixin, DeleteView):
    model = Event
    template_name = "events/confirm_delete.html"
    success_url = reverse_lazy("event_list")


# ─────────────────────────────────────────────
#  RSVP
# ─────────────────────────────────────────────

class RSVPView(LoginRequiredMixin, View):
    """POST to RSVP; handles both add and cancel via ?action= param."""

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        action = request.POST.get("action", "add")

        if action == "cancel":
            event.participants.remove(request.user)
            messages.success(request, f"Your RSVP for '{event.name}' has been cancelled.")
        else:
            if event.participants.filter(pk=request.user.pk).exists():
                messages.warning(request, "You have already RSVP'd to this event.")
            else:
                event.participants.add(request.user)
                messages.success(request, f"You've RSVP'd to '{event.name}'!")
                # Confirmation email is sent automatically via the m2m_changed signal

        return redirect("event_detail", pk=pk)