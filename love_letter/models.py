from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Mężczyzna'), ('K', 'Kobieta')], null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    interests = models.TextField(null=True, blank=True)
    lifestyle = models.CharField(max_length=50, null=True, blank=True)
    relationship_goal = models.CharField(max_length=50, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

class Like(models.Model):
    liker = models.ForeignKey(CustomUser, related_name='liker', on_delete=models.CASCADE)
    liked = models.ForeignKey(CustomUser, related_name='liked', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('liker', 'liked')

class Match(models.Model):
    user1 = models.ForeignKey(CustomUser, related_name='matcher1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(CustomUser, related_name='matcher2', on_delete=models.CASCADE)
    matched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')
