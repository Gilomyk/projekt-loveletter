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
    path('current_user/set', set_current_user_information, name='set_current_user_information'),
    path('lifestyles/', LifestyleList.as_view(), name='lifestyles-list'),
    path('relationship-goals/', RelationshipGoalList.as_view(), name='relationship-goals-list'),
    path('traits/', TraitList.as_view(), name='traits-list'),
    path('messages/<int:match_id>/', match_messages, name='match-messages'),
    path('messages/<int:match_id>/send/', send_message, name='send-message'),
    path('api/unlike/<int:liked_id>/', unlike_user, name='unlike-user'),
    path('update_current_user_profile/', update_current_user_profile, name='update_current_user_profile'),
    path('icebreaker/', get_random_icebreaker, name='get_random_icebreaker'),
    path('report/', submit_report, name='submit_report'),
    path('report/<int:id>/accept/', accept_report, name='accept_report'),
    path('report/<int:id>/deny/', deny_report, name='deny_report'),
    path('reports/', get_reports, name='get_reports'),
]