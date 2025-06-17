from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age', 'gender', 'location', 'interests', 'lifestyle', 'relationship_goal', 'profile_picture')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Like)
admin.site.register(Match)
admin.site.register(Lifestyle)
admin.site.register(RelationshipGoal)
admin.site.register(Trait)
admin.site.register(UserTrait)
admin.site.register(Message)
admin.site.register(Report)
admin.site.register(IcebreakerQuestion)