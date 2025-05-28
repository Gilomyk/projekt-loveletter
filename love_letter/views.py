'''
from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
def api_test(request):
    return JsonResponse({'message': 'u mnie działa xd'})
'''

from .models import *
from .serializers import *
from django.db import IntegrityError
from django.db.models import Q, Prefetch
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework import status

User = get_user_model()

class LifestyleList(generics.ListAPIView):
    queryset = Lifestyle.objects.all()
    serializer_class = LifestyleSerializer

class RelationshipGoalList(generics.ListAPIView):
    queryset = RelationshipGoal.objects.all()
    serializer_class = RelationshipGoalSerializer

class TraitList(generics.ListAPIView):
    queryset = Trait.objects.all()
    serializer_class = TraitSerializer


@api_view(['GET'])
def match_messages(request, match_id):
    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        return Response({'error': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)

    messages = match.get_messages()
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def send_message(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    # Tymczasowy sposób pobierania usera (np. bez logowania)
    sender_id = request.session.get('user_id')
    if not sender_id:
        return Response({'error': 'User not authenticated in session'}, status=401)

    if sender_id not in [match.user1.id, match.user2.id]:
        return Response({'error': 'You are not part of this match'}, status=403)

    receiver = match.user2 if sender_id == match.user1.id else match.user1

    serializer = CreateMessageSerializer(data=request.data)
    if serializer.is_valid():
        message = Message.objects.create(
            sender_id=sender_id,
            receiver=receiver,
            content=serializer.validated_data['content']
        )
        return Response(MessageSerializer(message).data, status=201)
    return Response(serializer.errors, status=400)
    
# Przeglądarka dla REST API
@api_view(['GET'])
def api_root(request, format=None):
    default_user_id = 1  # Przykładowe domyślne user_id
    return Response({
        'users': reverse('user_list', request=request, format=format),
        'preferences': reverse('get_user_preferences', request=request, format=format),
        'recommendations': reverse('user_recommendations', request=request, format=format),
        'matches': reverse('user_matches', request=request, format=format),
        'likes': reverse('user_likes', request=request, format=format),
        'switch_user(id=1)': reverse('switch_user', kwargs={'user_id': default_user_id}, request=request, format=format),
        'current_user': reverse('get_current_user', request=request, format=format),
        'messages(id=1)': reverse('match-messages', kwargs={'match_id': 1}, request=request, format=format),
        'send-message': reverse('send-message', kwargs={'match_id': 1}, request=request, format=format),
        'admin': 'http://localhost:8000/admin/',
    })

# (test moment) Pobieramy użytkowników, całe info
@api_view(['GET'])
def get_users(request):
    users = CustomUser.objects.all().prefetch_related(
        Prefetch('usertrait_set', queryset=UserTrait.objects.select_related('trait'))
    ).order_by('id')
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

# Zwróć użytkowników, których obecny user polubił
@api_view(['GET'])
def get_likes(request):
    current_user_id = request.session.get('user_id')
    if not current_user_id:
        return Response({'error': 'Brak aktywnego użytkownika.'}, status=status.HTTP_401_UNAUTHORIZED)

    likes = Like.objects.filter(liker_id=current_user_id).select_related('liked')

    liked_users = [{
        'id': like.liked.id,
        'username': like.liked.username,
        'first_name': like.liked.first_name,
        'age': like.liked.age,
        'profile_picture': 'http://localhost:8000' + like.liked.profile_picture.url if like.liked.profile_picture else None,
    } for like in likes]

    return Response(liked_users)

# Polub użytkownika
@api_view(['POST'])
def like_user(request, liked_id):
    current_user_id = request.session.get('user_id')
    if not current_user_id:
        return Response({'error': 'Brak aktywnego użytkownika.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if current_user_id == liked_id:
        return Response({'error': 'Nie możesz polubić samego siebie.'}, status=status.HTTP_400_BAD_REQUEST)

    liker = get_object_or_404(CustomUser, id=current_user_id)
    liked = get_object_or_404(CustomUser, id=liked_id)

    like, created = Like.objects.get_or_create(liker=liker, liked=liked)

    if not created:
        return Response({'message': 'Już polubiłeś tego użytkownika.'}, status=status.HTTP_200_OK)
    
    # Sprawdź, czy liked wcześniej polubił likera
    if Like.objects.filter(liker=liked, liked=liker).exists():
        # Tworzymy Match – uporządkujmy użytkowników po ID żeby uniknąć duplikatów
        user1, user2 = sorted([liker, liked], key=lambda u: u.id)
        try:
            Match.objects.create(user1=user1, user2=user2)
            return Response({'message': f'Match! {user1.username} i {user2.username} się polubili 🎉'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            # Match już istnieje (może z innego requesta?)
            return Response({'message': f'Match już istnieje między {user1.username} i {user2.username}.'}, status=status.HTTP_200_OK)

    return Response({'message': f'Użytkownik {liker.username} polubił {liked.username}.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def unlike_user(request, liked_id):
    current_user_id = request.session.get('user_id')
    if not current_user_id:
        return Response({'error': 'Brak aktywnego użytkownika.'}, status=status.HTTP_401_UNAUTHORIZED)

    liker = get_object_or_404(CustomUser, id=current_user_id)
    liked = get_object_or_404(CustomUser, id=liked_id)

    try:
        like = Like.objects.get(liker=liker, liked=liked)
        like.delete()
    except Like.DoesNotExist:
        return Response({'error': 'Nie polubiłeś tego użytkownika.'}, status=status.HTTP_400_BAD_REQUEST)

    # Usuwamy match jeśli istniał (niezależnie od kolejności userów)
    Match.objects.filter(
        models.Q(user1=liker, user2=liked) | models.Q(user1=liked, user2=liker)
    ).delete()

    return Response({'message': f'Usunięto polubienie i ewentualny match z {liked.username}.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_user_matches(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return Response({'error': 'Brak wybranego użytkownika'}, status=400)
    
    try:
        current_user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Użytkownik nie istnieje'}, status=404)

    matches = Match.objects.filter(Q(user1=current_user) | Q(user2=current_user))
    serializer = MatchSerializer(matches, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def get_user_preferences(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return Response({'error': 'Brak wybranego użytkownika w sesji'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Użytkownik nie istnieje'}, status=status.HTTP_404_NOT_FOUND)

    try:
        preference = Preference.objects.get(user=user)
    except Preference.DoesNotExist:
        return Response({'error': 'Brak ustawionych preferencji.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PreferenceSerializer(preference)
    return Response(serializer.data)

@api_view(['POST'])
def set_user_preferences(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return Response({'error': 'Brak wybranego użytkownika w sesji'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Użytkownik nie istnieje'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    try:
        # Pobierz lub utwórz preferencje użytkownika
        preference, created = Preference.objects.get_or_create(user=user)

        # Aktualizuj pola
        preference.preferred_gender = data.get('preferred_gender', preference.preferred_gender)
        preference.age_min = data.get('age_min', preference.age_min)
        preference.age_max = data.get('age_max', preference.age_max)
        preference.preferred_distance = data.get('preferred_distance', preference.preferred_distance)

        # Powiązania z innymi modelami
        lifestyle_id = data.get('preferred_lifestyle')
        if lifestyle_id:
            try:
                lifestyle = Lifestyle.objects.get(id=lifestyle_id)
                preference.preferred_lifestyle = lifestyle
            except Lifestyle.DoesNotExist:
                return Response({'error': 'Nieprawidłowy lifestyle'}, status=status.HTTP_400_BAD_REQUEST)

        goal_id = data.get('preferred_goal')
        if goal_id:
            try:
                goal = RelationshipGoal.objects.get(id=goal_id)
                preference.preferred_goal = goal
            except RelationshipGoal.DoesNotExist:
                return Response({'error': 'Nieprawidłowy cel'}, status=status.HTTP_400_BAD_REQUEST)

        # Hobbies (traity) - many to many
        hobby_ids = data.get('preferred_hobbies')
        if hobby_ids is not None:
            traits = Trait.objects.filter(id__in=hobby_ids)
            preference.preferred_hobbies.set(traits)

        preference.save()

        return Response({'message': 'Preferencje zapisane pomyślnie.'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_recommendations(request):
    print("rekomendacja dziala")
    
    user_id = request.session.get('user_id')
    if not user_id:
        return Response({'error': 'Brak wybranego użytkownika'}, status=400)
    
    try:
        current_user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Użytkownik nie istnieje'}, status=404)

    try:
        preference = Preference.objects.get(user=current_user)
    except Preference.DoesNotExist:
        return Response({'error': 'Brak ustawionych preferencji.'}, status=404)

    preferred_gender = preference.preferred_gender
    age_min = preference.age_min or 0
    age_max = preference.age_max or 89

    print("Płeć: ", preferred_gender)
    print("Maks. wiek: ", age_max)
    print("Min. wiek: ", age_min)

    recommended_users = CustomUser.objects.all().prefetch_related(
        Prefetch('usertrait_set', queryset=UserTrait.objects.select_related('trait'))
    ).filter(
        gender=preferred_gender,
        age__gte=age_min,
        age__lte=age_max,
    ).exclude(id=current_user.id)
    print("Po filtrze gender i age:", recommended_users.count())

    # print(preference.preferred_lifestyle)
    if preference.preferred_lifestyle:
        recommended_users = recommended_users.filter(lifestyle=preference.preferred_lifestyle)
        print("Po filtrze lifestyle:", recommended_users.count())

    # print (preference.preferred_goal)
    if preference.preferred_goal:
        recommended_users = recommended_users.filter(relationship_goal=preference.preferred_goal)
        print("Po filtrze goal:", recommended_users.count())

    # print([hobby.name for hobby in preference.preferred_hobbies.all()])
    if preference.preferred_hobbies.exists():
        recommended_users = recommended_users.filter(
            usertrait__trait__in=preference.preferred_hobbies.all()
        ).distinct()
        print("Po filtrze hobbies:", recommended_users.count())


    serializer = UserSerializer(recommended_users, many=True, context={'request': request})
    return Response(serializer.data)