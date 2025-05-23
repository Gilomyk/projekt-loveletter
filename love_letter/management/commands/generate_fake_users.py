from django.core.management.base import BaseCommand
from love_letter.models import CustomUser, Trait, Preference, Lifestyle, RelationshipGoal
from faker import Faker
import random
from django.core.files.base import ContentFile
import requests
from io import BytesIO

UNSPLASH_ACCESS_KEY = 'zrTnKSI2jUXvadA3yDi1a3pEnyPrt3eyLLrRnkmDd7w'

GENDER_CHOICES = ['M', 'K']

LIFESTYLES = ['Party Animal', 'Homebody', 'Married to the Grind', 'Academic Weapon', 'Wilderness Explorer']
DATING_GOALS = ['Still thinking about it', 'Long-term relationship', 'Short-term fun', 'Marriage']
HOBBIES = ['Climbing', 'Fencing', 'Computer Games', 'Coding', 'Hiking']


class Command(BaseCommand):
    help = 'Generate fake users for testing with preferences and traits'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of fake users to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        faker = Faker('pl_PL')

        # Ensure Lifestyle, RelationshipGoal, and Traits exist
        lifestyle_objs = {name: Lifestyle.objects.get_or_create(name=name)[0] for name in LIFESTYLES}
        goal_objs = {name: RelationshipGoal.objects.get_or_create(name=name)[0] for name in DATING_GOALS}
        hobby_objs = {name: Trait.objects.get_or_create(name=name)[0] for name in HOBBIES}

        for _ in range(count):
            gender = random.choice(GENDER_CHOICES)
            username = faker.user_name()
            first_name = faker.first_name_male() if gender == 'M' else faker.first_name_female()
            location = faker.city()
            lifestyle = random.choice(list(lifestyle_objs.values()))
            relationship_goal = random.choice(list(goal_objs.values()))
            hobbies = random.sample(list(hobby_objs.values()), k=random.randint(1, 3))

            user = CustomUser.objects.create_user(
                username=username,
                password='password123',
                first_name=first_name,
                age=random.randint(18, 40),
                gender=gender,
                location=location,
                lifestyle=lifestyle,
                relationship_goal=relationship_goal,
            )

            # Add profile picture
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

            # Assign user traits
            for trait in hobbies:
                user.usertrait_set.create(trait=trait)

            # Preferences
            pref = Preference.objects.create(
                user=user,
                preferred_gender=random.choice(GENDER_CHOICES),
                age_min=random.randint(18, 25),
                age_max=random.randint(26, 40),
                preferred_distance=random.choice([10, 20, 30, 50, 100]),
                preferred_lifestyle=random.choice(list(lifestyle_objs.values())),
                preferred_goal=random.choice(list(goal_objs.values())),
            )

            preferred_hobbies = random.sample(list(hobby_objs.values()), k=random.randint(1, 3))
            pref.preferred_hobbies.set(preferred_hobbies)

            self.stdout.write(self.style.SUCCESS(f'Utworzono użytkownika: {username}'))
