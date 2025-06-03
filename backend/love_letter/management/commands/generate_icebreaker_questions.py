from django.core.management.base import BaseCommand
from love_letter.models import CustomUser, Trait, Preference, Lifestyle, RelationshipGoal, IcebreakerQuestion
from faker import Faker
import random
from django.core.files.base import ContentFile
import requests
from io import BytesIO
import os

QUESTIONS = [
    'What is your number one date location?',
    'What was your dream job when you were little?',
    'Which country do you want to visit the most?',
    'If you could only eat one meal for the rest of your life, what would it be?',
    'Which country do you not want to visit at any cost?',
    'What present have you never gotten but desperately want?',
    'Whats your funniest dating app story?',
    'Whats a fun fact you just have to share?',
    'What are two truths and one lie about you?',
    'If you could become one animal what would it be?',
    'If you had a superpower what would it be?'
]

class Command(BaseCommand):
    help = 'Generate icebreaker questions'

    # def add_arguments(self, parser):
    #     parser.add_argument('count', type=int, help='Number of icebreaker questions to create', default=50)

    def handle(self, *args, **kwargs):
        count = 20

        for question in QUESTIONS:

            user = IcebreakerQuestion.objects.create(
                content=question
            )
