# Create your models here.
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser

class Lifestyle(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class RelationshipGoal(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Trait(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('M', 'Mężczyzna'), ('K', 'Kobieta')],
        null=True,
        blank=True
    )
    location = models.CharField(max_length=100, null=True, blank=True)
    hobbies = models.ManyToManyField(Trait, blank=True)
    lifestyle = models.ForeignKey(Lifestyle, null=True, blank=True, on_delete=models.SET_NULL)
    relationship_goal = models.ForeignKey(RelationshipGoal, null=True, blank=True, on_delete=models.SET_NULL)
    profile_picture = models.ImageField(upload_to='media/profile_pictures/', null=True, blank=True)

    language = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username
    
    @property
    def traits(self):
        # Zwraca queryset cech użytkownika (np. do porównania z preferencjami)
        return Trait.objects.filter(usertrait__user=self)

class Message(models.Model):
    sender = models.ForeignKey('CustomUser', related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey('CustomUser', related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} ➜ {self.receiver}: {self.content[:20]}"


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
    preferred_hobbies = models.ManyToManyField(Trait, blank=True)
    preferred_distance = models.PositiveIntegerField(null=True, blank=True)
    preferred_lifestyle = models.ForeignKey(Lifestyle, null=True, blank=True, on_delete=models.SET_NULL)
    preferred_goal = models.ForeignKey(RelationshipGoal, null=True, blank=True, on_delete=models.SET_NULL)

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

    # metoda zwracająca wiadomości dla danego matcha
    def get_messages(self):
        return Message.objects.filter(
            models.Q(sender=self.user1, receiver=self.user2) |
            models.Q(sender=self.user2, receiver=self.user1)
        ).order_by('timestamp')

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Match: {self.user1.username} & {self.user2.username}"
    
class Report(models.Model):
    reporter = models.ForeignKey(CustomUser, related_name='reporter', on_delete=models.CASCADE)
    reported = models.ForeignKey(CustomUser, related_name='reported', on_delete=models.CASCADE)
    reasoning = models.TextField()

    def __str__(self):
        return f"{self.reporter} ➜ {self.reported}: {self.reasoning[:20]}"
    
class IcebreakerQuestion(models.Model):
    content = models.TextField()

    def __str__(self):
        return f"{self.content[:75]}"