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
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

User = get_user_model()

# Przeglądarka dla REST API
@api_view(['GET'])
def api_root(request, format=None):
    default_user_id = 1  # Przykładowe domyślne user_id
    return Response({
        'users': reverse('user_list', request=request, format=format),
        'recommendations': reverse('user_recommendations', request=request, format=format),
        'matches': reverse('user_matches', request=request, format=format),
        'switch_user(id=1)': reverse('switch_user', kwargs={'user_id': default_user_id}, request=request, format=format),
        'current_user': reverse('get_current_user', request=request, format=format),
        'admin': '/admin/',
    })

# (test moment) Pobieramy użytkowników, całe info
@api_view(['GET'])
def get_users(request):
    users = CustomUser.objects.all().order_by('id')
    serializer = UserSerializer(users, many=True, context={'request': request})
    return Response(serializer.data)

# Endpointy do przełączania użytkownika
@api_view(['POST'])
def switch_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        request.session['user_id'] = user.id
        request.session.modified = True
        return Response({"message": f"User switched to {user.username}"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_current_user(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        return Response({"detail": "Brak wybranego użytkownika"}, status=404)
    try:
        user = CustomUser.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response({"detail": "Użytkownik nie istnieje"}, status=404)



@api_view(['GET'])
def get_user_matches(request):
    current_user = CustomUser.objects.get(id=1)  # Na sztywno
    matches = Match.objects.filter(Q(user1=current_user) | Q(user2=current_user))
    serializer = MatchSerializer(matches, many=True, context={'request': request})
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