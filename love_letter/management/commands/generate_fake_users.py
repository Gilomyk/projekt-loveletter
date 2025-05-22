from django.core.management.base import BaseCommand
from love_letter.models import CustomUser, Trait, Preference
from faker import Faker
import random
from django.core.files.base import ContentFile
import requests
from io import BytesIO

UNSPLASH_ACCESS_KEY = 'zrTnKSI2jUXvadA3yDi1a3pEnyPrt3eyLLrRnkmDd7w'

GENDER_CHOICES = ['M', 'K']
LIFESTYLES = ['lifestyle0', 'lifestyle1', 'lifestyle2', 'lifestyle3', 'lifestyle4'] #
DATING_GOALS = ['dating_goal0', 'dating_goal1', 'dating_goal2', 'dating_goal3']
HOBBIES = ['hobby0', 'hobby1', 'hobby2', 'hobby3', 'hobby4']

class Command(BaseCommand):
    help = 'Generate fake users for testing with preferences and traits'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of fake users to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        faker = Faker('pl_PL') #polskie imiona, miasta itp.

        # Upewnij się, że cechy (hobby) istnieją w bazie
        for hobby in HOBBIES:
            Trait.objects.get_or_create(name=hobby)

        for _ in range(count):
            gender = random.choice(GENDER_CHOICES)
            username = faker.user_name()
            first_name = faker.first_name_male() if gender == 'M' else faker.first_name_female()
            location = faker.city()
            lifestyle = random.choice(LIFESTYLES)
            relationship_goal = random.choice(DATING_GOALS)
            interests = random.sample(HOBBIES, k=random.randint(1, 3))

            user = CustomUser.objects.create_user(
                username=username,
                password='password123',  # tymczasowe hasło (niepotrzebne teraz)
                first_name=first_name,
                age=random.randint(18, 40),
                gender=gender,
                location=location,
                interests=', '.join(interests),
                lifestyle=lifestyle,
                relationship_goal=relationship_goal,
            )

            # Dodaj zdjęcie profilowe z Unsplash
            try:
                response = requests.get(
                    f"https://api.unsplash.com/photos/random?client_id={UNSPLASH_ACCESS_KEY}&query=portrait"
                )
                data = response.json()
                photo_url = data['urls']['regular']
                img_response = requests.get(photo_url)
                img_content = BytesIO(img_response.content)
                img_name = f'{username}_profile.jpg'
                user.profile_picture.save(img_name, ContentFile(img_content.read()), save=True)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Błąd przy pobieraniu zdjęcia dla {username}: {e}'))

            # Dodaj cechy (traity)
            for interest in interests:
                trait_obj = Trait.objects.get(name=interest)
                user.usertrait_set.create(trait=trait_obj)

            # Dodaj preferencje użytkownika
            pref = Preference.objects.create(
                user=user,
                preferred_gender=random.choice(GENDER_CHOICES),
                age_min=random.randint(18, 25),
                age_max=random.randint(26, 40),
                preferred_distance=random.choice([10, 20, 30, 50, 100]),
                preferred_lifestyle=random.choice(LIFESTYLES),
                preferred_goal=random.choice(DATING_GOALS),
            )
            # Dodaj preferowane hobby do preferencji
            preferred_hobbies = random.sample(HOBBIES, k=random.randint(1, 3))
            for hobby in preferred_hobbies:
                trait = Trait.objects.get(name=hobby)
                pref.preferred_hobbies.add(trait)

            self.stdout.write(self.style.SUCCESS(f'Utworzono użytkownika: {username}'))
