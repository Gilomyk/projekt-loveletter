from django.core.management.base import BaseCommand
from love_letter.models import CustomUser
from faker import Faker
import random
from django.core.files.base import ContentFile
import requests
from io import BytesIO
from django.conf import settings

UNSPLASH_ACCESS_KEY     = 'zrTnKSI2jUXvadA3yDi1a3pEnyPrt3eyLLrRnkmDd7w'

class Command(BaseCommand):
    help = 'Generate fake users for testing'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of fake users to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        faker = Faker('pl_PL')  # polskie imiona, miasta itp.

        for _ in range(count):
            gender = random.choice(['M', 'K'])
            username = faker.user_name()
            first_name = faker.first_name_male() if gender == 'M' else faker.first_name_female()
            location = faker.city()
            interests = ', '.join(faker.words(nb=3))
            lifestyle = random.choice(['aktywny', 'spokojny', 'zbalansowany'])
            relationship_goal = random.choice(['przyjaźń', 'związek', 'randki', 'nie wiem'])

            # Utwórz użytkownika
            user = CustomUser.objects.create_user(
                username=username,
                password='password123',  # tymczasowe hasło (niepotrzebne teraz)
                first_name=first_name,
                age=random.randint(18, 40),
                gender=gender,
                location=location,
                interests=interests,
                lifestyle=lifestyle,
                relationship_goal=relationship_goal,
            )

            # Pobranie zdjęcia z Unsplash
            try:
                response = requests.get(
                f"https://api.unsplash.com/photos/random?client_id={UNSPLASH_ACCESS_KEY}&query=portrait"
                )

                data = response.json()
                photo_url = data['urls']['regular']

                # teraz możesz pobierać zdjęcie jak wcześniej:
                img_response = requests.get(photo_url)
                img_content = BytesIO(img_response.content)
                img_name = f'{username}_profile.jpg'
                user.profile_picture.save(img_name, ContentFile(img_content.read()), save=True)
                self.stdout.write(self.style.SUCCESS(f'Utworzono użytkownika: {username} z obrazkiem.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Błąd przy pobieraniu zdjęcia dla {username}: {e}'))
