# 🎉 Event Management System (Django + Tailwind)

A full-featured **Event Management Web Application** built with **Django (Backend)** and **Tailwind CSS (Frontend)**.
This project supports **role-based access control**, **RSVP system**, **email activation**, and **user profile management**.

---

# 🚀 Features Overview

## 🔐 1. Authentication System

* User Registration (Signup)
* Login & Logout
* Email-based Account Activation
* Password Reset via Email

---

## 👥 2. Role-Based Access Control (RBAC)

Using **Django Groups**, users are assigned roles:

### 🛡️ Admin

* Full system control
* Manage users, roles, and groups
* View all participants
* Create/Delete groups
* Assign roles

### 🧑‍💼 Organizer

* Create, update, delete:

  * Events
  * Categories
* Access Organizer Dashboard

### 👤 Participant

* View events
* RSVP to events
* View personal RSVP list (Dashboard)

---

## 📅 3. Event Management

* Create Events (Organizer only)
* Update/Delete Events
* Category-based organization
* Event Image support (with default image)

---

## ✅ 4. RSVP System

* Users can RSVP to events
* Prevent duplicate RSVP
* Cancel RSVP
* ManyToMany relationship:

  ```
  User ↔ Event
  ```
* Confirmation email via Django Signals

---

## 📧 5. Email System

* Account activation email
* RSVP confirmation email
* Password reset email

---

## 🔄 6. Django Signals

Automated processes:

* Send activation email after signup
* Send RSVP confirmation email

---

## 🧑‍💻 7. User Profile System

* View Profile
* Edit Profile:

  * First Name
  * Last Name
  * Profile Picture
  * Phone Number
* Change Password
* Reset Password via Email

---

## 🧱 8. Custom User Model

```python
class CustomUser(AbstractUser):
    profile_picture = models.ImageField(...)
    phone_number = models.CharField(...)
```

---

## 📊 9. Dashboards

### Admin Dashboard

* Manage users
* Assign roles
* View participants

### Organizer Dashboard

* Event statistics
* Manage events & categories

### Participant Dashboard

* View RSVP’d events

---

# 🏗️ Project Structure

```
event_management/
│
├── core/                  # Common views/templates
├── events/                # Event & Category logic
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│
├── users/                 # Authentication & profile
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│       ├── admin/
│       ├── users/
│
├── templates/
│   ├── base.html
│   ├── navbar/
│
├── static/
├── media/
├── populate_db.py
```

---

# ⚙️ Setup Instructions

## 1️⃣ Clone Project

```bash
git clone <repo-url>
cd event_management
```

## 2️⃣ Create Virtual Environment

```bash
python -m venv event_env
source event_env/Scripts/activate   # Windows
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 5️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

## 6️⃣ Run Server

```bash
python manage.py runserver
```

---

# 🧪 Populate Database (Optional)

```bash
python populate_db.py
```

Creates:

* Categories (5–6)
* Events (20–25)
* Users (Participants)

---

# 🖼️ Media Configuration

### settings.py

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### urls.py

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

# 🎨 Frontend

* Tailwind CSS
* Responsive Design
* Role-based dynamic navbar
* Modern card UI

---

# 🔐 Permissions Logic

| Feature       | Admin | Organizer | Participant |
| ------------- | ----- | --------- | ----------- |
| Manage Users  | ✅     | ❌         | ❌           |
| Manage Events | ✅     | ✅         | ❌           |
| View Events   | ✅     | ✅         | ✅           |
| RSVP          | ❌     | ❌         | ✅           |

---

# ⚠️ Important Notes

* Use **CustomUser** instead of default User
* Ensure **Groups exist**:

  * Admin
  * Organizer
  * Participant
* Email settings must be configured for activation/reset

---

# 🔥 Future Improvements

* Notification system 🔔
* Event search & filters 🔍
* Payment integration 💳
* Real-time RSVP updates ⚡
* REST API (DRF) 🌐

---

# 👨‍💻 Author

**Sakir Mohammad Safayet**

---

# 💡 Conclusion

This project demonstrates:

* Full-stack Django development
* Clean architecture
* Role-based system design
* Real-world features implementation

---

⭐ If you like this project, give it a star!
