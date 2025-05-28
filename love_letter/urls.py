from django.urls import path
from .views import (
    get_users,
    get_user_recommendations,
    get_user_matches,
    get_likes,
    like_user,
    switch_user,
    get_current_user,
    set_current_user_information,
    get_user_preferences,
    set_user_preferences,
    LifestyleList,
    RelationshipGoalList,
    TraitList,
)

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
]