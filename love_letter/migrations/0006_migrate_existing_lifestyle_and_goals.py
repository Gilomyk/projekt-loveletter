from django.db import migrations


def migrate_lifestyle_and_goal(apps, schema_editor):
    CustomUser = apps.get_model('love_letter', 'CustomUser')
    Preference = apps.get_model('love_letter', 'Preference')
    Lifestyle = apps.get_model('love_letter', 'Lifestyle')
    RelationshipGoal = apps.get_model('love_letter', 'RelationshipGoal')

    # Zbierz wszystkie unikalne stringi lifestyle i goal
    user_lifestyles = set(CustomUser.objects.exclude(lifestyle__isnull=True).values_list('lifestyle', flat=True))
    pref_lifestyles = set(Preference.objects.exclude(preferred_lifestyle__isnull=True).values_list('preferred_lifestyle', flat=True))
    all_lifestyles = user_lifestyles.union(pref_lifestyles)

    user_goals = set(CustomUser.objects.exclude(relationship_goal__isnull=True).values_list('relationship_goal', flat=True))
    pref_goals = set(Preference.objects.exclude(preferred_goal__isnull=True).values_list('preferred_goal', flat=True))
    all_goals = user_goals.union(pref_goals)

    # Utwórz Lifestyle
    lifestyle_map = {}
    for name in all_lifestyles:
        if not name:
            continue
        obj, _ = Lifestyle.objects.get_or_create(name=name)
        lifestyle_map[name] = obj

    # Utwórz RelationshipGoal
    goal_map = {}
    for name in all_goals:
        if not name:
            continue
        obj, _ = RelationshipGoal.objects.get_or_create(name=name)
        goal_map[name] = obj

    # Zaktualizuj użytkowników
    for user in CustomUser.objects.all():
        if user.lifestyle and user.lifestyle in lifestyle_map:
            user.lifestyle = lifestyle_map[user.lifestyle]
        if user.relationship_goal and user.relationship_goal in goal_map:
            user.relationship_goal = goal_map[user.relationship_goal]
        user.save()

    # Zaktualizuj preferencje
    for pref in Preference.objects.all():
        if pref.preferred_lifestyle and pref.preferred_lifestyle in lifestyle_map:
            pref.preferred_lifestyle = lifestyle_map[pref.preferred_lifestyle]
        if pref.preferred_goal and pref.preferred_goal in goal_map:
            pref.preferred_goal = goal_map[pref.preferred_goal]
        pref.save()


class Migration(migrations.Migration):

    dependencies = [
        ('love_letter', '0005_customuser_interests_customuser_location_and_more'),
    ]

    operations = [
        migrations.RunPython(migrate_lifestyle_and_goal),
    ]
