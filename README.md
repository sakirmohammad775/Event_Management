# EventHub — Event Management Platform

A full-stack event management system built with Django and Tailwind CSS. Supports role-based access, RSVP workflows, email automation, and user profile management.
---

## Live Link : https://event-management-na8a.onrender.com/
## Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11 / Django 5.0 |
| Frontend | Tailwind CSS |
| Database | PostgreSQL (production) / SQLite3 (development) |
| Auth | Custom AbstractUser model |
| Automation | Django Signals |

---
## Users(For testing purpose)
- Orgnizer -> username: stone,Password: stone12345
- Participant -> username: test,Password: test12345

## Features

### Authentication
- Signup with email, first/last name, username
- Email-based account activation via signed tokens
- Login, logout, password change and reset

### Role-Based Access Control
Three roles managed through Django Groups:

| Feature | Admin | Organizer | Participant |
|---|:---:|:---:|:---:|
| Manage users & roles | ✅ | ❌ | ❌ |
| Create/edit events | ✅ | ✅ | ❌ |
| View events | ✅ | ✅ | ✅ |
| RSVP to events | ❌ | ❌ | ✅ |

### Events
- Full CRUD for events and categories (Organizer/Admin)
- Event image upload with default image fallback
- `select_related` and `prefetch_related` for optimised queries

### RSVP System
- One-click RSVP with duplicate prevention
- Cancel RSVP from participant dashboard
- ManyToMany relationship between `User` and `Event`
- Confirmation email via Django Signals

### Email Automation (Django Signals)
- Activation email on signup (`post_save`)
- RSVP confirmation on registration (`m2m_changed`)

### User Profiles
- View and edit profile (name, avatar, phone number)
- Change password
- Email-based password reset

---

## Project Structure
```
event_management/
│
├── core/                            # Landing page, shared UI
│   ├── views.py
│   ├── urls.py
│   └── templates/core/
│       ├── base.html                # Master layout, role-based navbar switching
│       ├── navbar_admin.html
│       ├── navbar_organizer.html
│       ├── navbar_participant.html
│       ├── navbar_non_logged.html
│       ├── home.html
│       ├── card.html                # Reusable event card partial
│       ├── footer.html
│       └── non_permission.html
│
├── events/                          # Event and category management
│   ├── models.py                    # Event, Category
│   ├── views.py                     # All CBVs: List, Detail, Create, Update, Delete, RSVP
│   ├── forms.py
│   ├── urls.py
│   ├── signals.py                   # RSVP confirmation email (m2m_changed)
│   └── templates/
│       ├── events/
│       │   ├── event_list.html
│       │   ├── event_detail.html
│       │   ├── event_card.html      # Reusable list card partial
│       │   ├── category_list.html
│       │   ├── form.html            # Shared create/update form
│       │   └── confirm_delete.html
│       └── dashboard/
│           ├── dashboard.html            # Base dashboard layout (extended by all dashboards)
│           ├── organizer_dashboard.html
│           ├── admin_dashboard.html
│           └── participant_dashboard.html
│
├── users/                           # Auth, profiles, RBAC
│   ├── models.py                    # CustomUser (AbstractUser + profile_picture + phone_number)
│   ├── views.py                     # SignUpView, SignInView, ActivateUserView, ProfileView, etc.
│   ├── forms.py
│   ├── urls.py
│   ├── signals.py                   # Activation email (post_save) + RSVP email connector
│   ├── apps.py                      # Registers both signals in ready()
│   └── templates/
│       ├── users/
│       │   ├── signup.html
│       │   └── signin.html
│       ├── admin/
│       │   ├── dashboard.html
│       │   ├── assign_role.html
│       │   ├── create_group.html
│       │   ├── group_list.html
│       │   └── participant_list.html
│       └── profile/
│           ├── profile.html
│           ├── edit_profile.html
│           └── change_password.html
│
├── media/                           # Uploaded files (gitignored)
│   ├── profile_pics/
│   ├── events_asset/
│   └── defaults/                    # Default images committed to repo
│
├── static/                          # CSS, JS, static images
├── event_management/                # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── populate_db.py                   # Seeds 5 categories + 20 events
├── requirements.txt
├── build.sh                         # Render build script
├── render.yaml                      # Render deployment config
├── .env                             # Local env vars (gitignored)
└── manage.py
```
---
### User Journey
1. Register → Activation email sent automatically (post_save signal)
2. Click email link → Account activated → Redirect to Sign In
3. Sign In → Redirected to role-specific dashboard
4. Participant browses events → RSVPs to an event
5. Confirmation email sent (m2m_changed signal)
6. Event appears in Participant Dashboard with cancel option
7. Organizer creates / manages events from Organizer Dashboard
8. Admin assigns roles and manages users from Admin Dashboard
---
## Setup

```bash
# 1. Clone and enter project
git clone https://github.com/your-username/eventhub.git
cd eventhub

# 2. Create and activate virtual environment
python -m venv event_env
source event_env/Scripts/activate   # Windows
source event_env/bin/activate       # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
# Create a .env file in the project root:
# SECRET_KEY=your-secret-key
# DEBUG=True
# EMAIL_HOST_USER=your@gmail.com
# EMAIL_HOST_PASSWORD=yourgmailapppassword
# FRONTEND_URL=http://localhost:8000

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. (Optional) Seed the database
python populate_db.py

# 8. Start the server
python manage.py runserver
```

---

## Environment Variables

| Key | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for development, `False` for production |
| `DATABASE_URL` | PostgreSQL URL (Render sets this automatically) |
| `EMAIL_HOST_USER` | Gmail address |
| `EMAIL_HOST_PASSWORD` | Gmail App Password (no spaces) |
| `FRONTEND_URL` | Base URL for activation links |

---

## Deployment (Render)

```bash
# Build command
./build.sh

# Start command
gunicorn event_management.wsgi:application
```

Set all environment variables in the Render dashboard. Add a PostgreSQL database and connect it via `DATABASE_URL`.

---

## Seed Data

Running `python populate_db.py` creates:
- 5 categories
- 20+ events with images
- Sample participant accounts

---

## Author

**Sakir Mohammad Safayet** — Full-Stack Developer

---

> Built as a demonstration of full-stack Django development, clean role-based architecture, and real-world feature implementation.
