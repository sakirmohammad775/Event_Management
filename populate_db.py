import os
import django
import random
from faker import Faker

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from events.models import Event, Category, Participant


def populate_db():
    fake = Faker()

    # -------- Create Categories (5) --------
    categories = []
    for _ in range(5):
        category = Category.objects.create(
            name=fake.word().capitalize(),
            description=fake.sentence()
        )
        categories.append(category)

    print(f"Created {len(categories)} categories")

    # -------- Create Events (20–25) --------
    events = []
    for _ in range(random.randint(20, 25)):
        event = Event.objects.create(
            name=fake.sentence(nb_words=3),
            description=fake.paragraph(),
            date=fake.date_between(start_date='-30d', end_date='+30d'),
            time=fake.time(),
            location=fake.city(),
            category=random.choice(categories)
        )
        events.append(event)

    print(f"Created {len(events)} events")

    # -------- Create Participants (20–30) --------
    participants = []
    for _ in range(random.randint(20, 30)):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.unique.email()
        )
        # Assign participant to 1–3 random events
        participant.events.set(
            random.sample(events, random.randint(1, 3))
        )
        participants.append(participant)

    print(f"Created {len(participants)} participants")

    print("✅ Database populated successfully!")


if __name__ == "__main__":
    populate_db()
