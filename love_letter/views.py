'''
from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
def api_test(request):
    return JsonResponse({'message': 'u mnie działa xd'})
'''
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser, Preference, Match
from .serializers import MatchSerializer, UserSerializer
from django.db.models import Q

# (test moment) Pobieramy użytkowników, całe info
@api_view(['GET'])
def get_users(request):
    users = CustomUser.objects.all().order_by('id')
    serializer = UserSerializer(users, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def get_user_matches(request):
    current_user = CustomUser.objects.get(id=1)  # Na sztywno
    matches = Match.objects.filter(Q(user1=current_user) | Q(user2=current_user))
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_user_recommendations(request):
    print("rekomendacja dziala")
    current_user = CustomUser.objects.get(id=1)

    try:
        preference = Preference.objects.get(user=current_user)
    except Preference.DoesNotExist:
        return Response({'error': 'Brak ustawionych preferencji.'}, status=404)

    preferred_gender = preference.preferred_gender
    age_min = preference.age_min or 0
    age_max = preference.age_max or 150

    recommended_users = CustomUser.objects.filter(
        gender=preferred_gender,
        age__gte=age_min,
        age__lte=age_max
    ).exclude(id=current_user.id)

    serializer = UserSerializer(recommended_users, many=True)
    return Response(serializer.data)