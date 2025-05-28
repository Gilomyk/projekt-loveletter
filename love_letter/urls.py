from django.urls import path
from .views import *

urlpatterns = [
    path('users/', get_users, name='user_list'),
    path('chat/', get_user_matches, name='user_matches'),
    path('likes/', get_likes, name='user_likes'),
    path('like/<int:liked_id>/', like_user, name='like_user'),
    path('switch_user/<int:user_id>/', switch_user, name='switch_user'),
    path('get_current_user/', get_current_user, name='get_current_user'),
    path('preferences/', get_user_preferences, name='get_user_preferences'),
    path('preferences/set/', set_user_preferences, name='set_user_preferences'),
    path('recommendations/', get_user_recommendations, name='user_recommendations'),
    path('lifestyles/', LifestyleList.as_view(), name='lifestyles-list'),
    path('relationship-goals/', RelationshipGoalList.as_view(), name='relationship-goals-list'),
    path('traits/', TraitList.as_view(), name='traits-list'),
    path('messages/<int:match_id>/', match_messages, name='match-messages'),
    path('messages/<int:match_id>/send/', send_message, name='send-message'),
]