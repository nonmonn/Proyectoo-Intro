# Generated by Django 5.1.1 on 2024-11-13 03:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_delete_recommendation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userquizresponse',
            name='date_submitted',
        ),
        migrations.RemoveField(
            model_name='userquizresponse',
            name='is_correct',
        ),
    ]
