from django.urls import path
from .views import (
    get_users,
    get_user_recommendations,
    get_user_matches,
    switch_user,
    get_current_user
)

urlpatterns = [
    path('recommendations/', get_user_recommendations, name='user_recommendations'),
    path('users/', get_users, name='user_list'),
    path('chat/', get_user_matches, name='user_matches'),
    path('switch_user/<int:user_id>/', switch_user, name='switch_user'),
    path('get_current_user/', get_current_user, name='get_current_user'),
]