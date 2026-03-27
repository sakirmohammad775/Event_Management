import os
import django
import random
from faker import Faker

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from events.models import Event, Category
from django.contrib.auth import get_user_model

User = get_user_model()


def populate_db():
    fake = Faker()

    # -------- Create Users (Participants) --------
    users = []
    for _ in range(random.randint(10, 12)):
        user = User.objects.create_user(
            username=fake.unique.user_name(),
            email=fake.unique.email(),
            password="12345678",
            phone_number=f"01{random.randint(300000000, 999999999)}"
        )
        users.append(user)

    print(f"Created {len(users)} users (participants)")

    # -------- Create Categories (5-6) --------
    categories = []
    for _ in range(random.randint(5, 6)):
        category = Category.objects.create(
            name=fake.unique.word().capitalize(),
            description=fake.sentence()
        )
        categories.append(category)

    print(f"Created {len(categories)} categories")

    # -------- Create Events (20–25) --------
    events = []
    for i in range(random.randint(7, 10)):
        print(f"Creating event {i+1}...")   # 👈 ADD THIS

        event = Event.objects.create(
            name=fake.sentence(nb_words=3),
            description=fake.paragraph(),
            date=fake.date_between(start_date='-10d', end_date='+30d'),
            time=fake.time(),
            location=fake.city(),
            category=random.choice(categories),
    )

        selected_users = random.sample(users, random.randint(2, min(6, len(users))))
        event.participants.set(selected_users)

        print(f"Event {i+1} created with participants")  # 👈 ADD THIS

    print(f"Created {len(events)} events")

    print("✅ Database populated successfully!")


if __name__ == "__main__":
    populate_db()