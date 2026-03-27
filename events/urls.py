from django.urls import path
from events.views import (
    # Dashboards
    OrganizerDashboardView,
    ParticipantDashboardView,

    # Category CRUD
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,

    # Event CRUD
    EventListView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,

    # RSVP
    RSVPView,
)

urlpatterns = [
    # ── Dashboards ──────────────────────────────────
    path("dashboard/organizer/", OrganizerDashboardView.as_view(), name="organizer_dashboard"),
    path("dashboard/participant/", ParticipantDashboardView.as_view(), name="participant_dashboard"),

    # ── Events ──────────────────────────────────────
    path("", EventListView.as_view(), name="event_list"),
    path("create/", EventCreateView.as_view(), name="event_create"),
    path("<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path("<int:pk>/update/", EventUpdateView.as_view(), name="event_update"),
    path("<int:pk>/delete/", EventDeleteView.as_view(), name="event_delete"),

    # ── RSVP ────────────────────────────────────────
    path("<int:pk>/rsvp/", RSVPView.as_view(), name="rsvp_event"),

    # ── Categories ──────────────────────────────────
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("categories/create/", CategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>/update/", CategoryUpdateView.as_view(), name="category_update"),
    path("categories/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category_delete"),
]