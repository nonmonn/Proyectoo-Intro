# Generated by Django 5.1.1 on 2024-11-13 03:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_remove_achievement_reward_remove_achievement_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Recommendation',
        ),
    ]
