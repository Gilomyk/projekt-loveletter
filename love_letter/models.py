# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('M', 'Mężczyzna'), ('K', 'Kobieta')],
        null=True,
        blank=True
    )
    location = models.CharField(max_length=100, null=True, blank=True)
    interests = models.TextField(null=True, blank=True)
    lifestyle = models.CharField(max_length=50, null=True, blank=True)
    relationship_goal = models.CharField(max_length=50, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.username

class Trait(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class UserTrait(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'trait')

    def __str__(self):
        return f"{self.user.username} - {self.trait.name}"

class Preference(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    preferred_gender = models.CharField(
        max_length=10,
        choices=[('M', 'Mężczyzna'), ('K', 'Kobieta')],
        null=True,
        blank=True
    )
    age_min = models.PositiveIntegerField(null=True, blank=True)
    age_max = models.PositiveIntegerField(null=True, blank=True)
    preferred_traits = models.ManyToManyField(Trait, blank=True)

    def __str__(self):
        return f"Preferencje {self.user.username}"

class Like(models.Model):
    liker = models.ForeignKey(CustomUser, related_name='liker', on_delete=models.CASCADE)
    liked = models.ForeignKey(CustomUser, related_name='liked', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('liker', 'liked')

    def __str__(self):
        return f"{self.liker.username} polubił {self.liked.username}"

class Match(models.Model):
    user1 = models.ForeignKey(CustomUser, related_name='matcher1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(CustomUser, related_name='matcher2', on_delete=models.CASCADE)
    matched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Match: {self.user1.username} & {self.user2.username}"
