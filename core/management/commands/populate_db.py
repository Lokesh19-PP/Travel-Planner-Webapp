import random
import os
import requests
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from faker import Faker
from core.models import Destination, Itinerary, Review, Favorite, ItineraryDay, Activity
from django.core.files.base import ContentFile

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with demo data and real images'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data...')
        Activity.objects.all().delete()
        ItineraryDay.objects.all().delete()
        Favorite.objects.all().delete()
        Review.objects.all().delete()
        Itinerary.objects.all().delete()
        Destination.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Downloading travel images...')
        image_data = [] # List of (filename, content)
        # 10 generic travel search terms
        search_terms = ['paris', 'tokyo', 'beach', 'mountain', 'forest', 'cityscape', 'desert', 'tropical', 'europe', 'asia']
        for i, term in enumerate(search_terms * 2): # Download 20 images
            try:
                response = requests.get(f'https://loremflickr.com/800/600/travel,{term}', timeout=10)
                if response.status_code == 200:
                    image_data.append((f'demo_{i}.jpg', response.content))
                    self.stdout.write(f'Downloaded image {i+1}/20 for "{term}"')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Failed to download image {i+1}: {e}'))

        self.stdout.write('Creating users...')
        users = []
        for _ in range(20):
            username = fake.user_name()
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=fake.email(),
                    password='password123'
                )
                users.append(user)

        self.stdout.write('Creating destinations...')
        countries = [fake.country() for _ in range(30)]
        price_ranges = ['$', '$$', '$$$'] # Consistent with UI filters
        destinations = []

        for i in range(100):
            name = fake.city()
            # Ensure unique name for slug
            while any(d.name == name for d in destinations):
                name = fake.city() + f" {i}"

            dest = Destination(
                name=name,
                country=random.choice(countries),
                description=fake.paragraph(nb_sentences=5),
                price_range=random.choice(price_ranges),
                rating=random.uniform(3.0, 5.0),
                tag=fake.word()
            )
            
            if image_data:
                img_name, img_content = random.choice(image_data)
                dest.image.save(img_name, ContentFile(img_content), save=False)
            
            dest.save()
            destinations.append(dest)

        self.stdout.write('Creating itineraries...')
        for _ in range(50):
            user = random.choice(users)
            num_dests = random.randint(1, 5)
            selected_dests = random.sample(destinations, num_dests)
            
            start_date = fake.date_between(start_date='today', end_date='+1y')
            end_date = start_date + timezone.timedelta(days=random.randint(3, 10))
            
            itinerary = Itinerary.objects.create(
                user=user,
                name=f"Trip to {selected_dests[0].name}" if len(selected_dests) == 1 else f"Adventure in {selected_dests[0].country}",
                start_date=start_date,
                end_date=end_date
            )
            itinerary.destinations.set(selected_dests)
            
            # Create days
            num_days = (end_date - start_date).days + 1
            for d in range(1, num_days + 1):
                day = ItineraryDay.objects.get_or_create(
                    itinerary=itinerary,
                    day_number=d
                )[0]
                day.notes = fake.sentence()
                day.save()
                
                # Create 2-4 activities per day
                for _ in range(random.randint(2, 4)):
                    Activity.objects.create(
                        day=day,
                        title=fake.catch_phrase(),
                        description=fake.sentence(),
                        time=timezone.now().time(),
                        cost=random.uniform(10, 200)
                    )

        self.stdout.write('Creating reviews...')
        for _ in range(200):
            user = random.choice(users)
            dest = random.choice(destinations)
            Review.objects.create(
                user=user,
                destination=dest,
                rating=random.randint(3, 5),
                comment=fake.paragraph()
            )

        self.stdout.write('Creating favorites...')
        for _ in range(150):
            user = random.choice(users)
            dest = random.choice(destinations)
            Favorite.objects.get_or_create(user=user, destination=dest)

        self.stdout.write(self.style.SUCCESS(f'Successfully populated database with 100 destinations, 50 itineraries, and real images.'))
