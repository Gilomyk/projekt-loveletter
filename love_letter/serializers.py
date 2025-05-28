from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    username = serializers.CharField(source='__str__', read_only=True)

    # Zakładam, że to ManyToMany lub ForeignKey, więc dodajemy serializery relacji:
    lifestyle = serializers.SerializerMethodField()
    relationship_goal = serializers.SerializerMethodField()
    hobbies = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'age', 'gender', 'location', 'profile_picture', 'lifestyle', 'relationship_goal', 'hobbies']

    def get_profile_picture(self, obj):
        request = self.context.get('request')
        if obj.profile_picture and hasattr(obj.profile_picture, 'url'):
            if request:
                return request.build_absolute_uri(obj.profile_picture.url)
            return obj.profile_picture.url
        return ''

    def get_lifestyle(self, obj):
        # jeśli lifestyle jest ForeignKey
        if obj.lifestyle:
            return {'id': obj.lifestyle.id, 'name': obj.lifestyle.name}
        return None

    def get_relationship_goal(self, obj):
        # jeśli goal jest ForeignKey
        if obj.relationship_goal:
            return {'id': obj.relationship_goal.id, 'name': obj.relationship_goal.name}
        return None

    def get_hobbies(self, obj):
        # Jeśli przekazano z kontekstu prefetchowane dane, użyj ich:
        user_traits = getattr(obj, 'usertrait_set', None)
        if user_traits and hasattr(user_traits, 'all'):
            return [{'id': ut.trait.id, 'name': ut.trait.name} for ut in user_traits.all()]

        # W przeciwnym razie – zapytanie awaryjne
        return [{'id': ut.trait.id, 'name': ut.trait.name}
                for ut in UserTrait.objects.filter(user=obj).select_related('trait')]


class MatchSerializer(serializers.ModelSerializer):
    user1 = UserSerializer()
    user2 = UserSerializer()

    class Meta:
        model = Match
        fields = ['id', 'user1', 'user2', 'matched_at']

class LikeSerializer(serializers.ModelSerializer):
    liker = UserSerializer()
    liked = UserSerializer()

    class Meta:
        model = Like
        fields = ['id', 'liker', 'liked', 'created_at']

class TraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trait
        fields = ['id', 'name']

class LifestyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lifestyle
        fields = ['id', 'name']

class RelationshipGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationshipGoal
        fields = ['id', 'name']

class PreferenceSerializer(serializers.ModelSerializer):
    preferred_hobbies = TraitSerializer(many=True)
    preferred_lifestyle = LifestyleSerializer()
    preferred_goal = RelationshipGoalSerializer()

    class Meta:
        model = Preference
        fields = [
            'preferred_gender',
            'age_min',
            'age_max',
            'preferred_distance',
            'preferred_lifestyle',
            'preferred_goal',
            'preferred_hobbies',
        ]

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'is_read']

class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content']
