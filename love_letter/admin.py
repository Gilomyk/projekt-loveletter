from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Like, Match

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'gender', 'location', 'interests', 'lifestyle', 'relationship_goal', 'profile_picture')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Like)
admin.site.register(Match)