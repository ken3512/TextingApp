# Generated by Django 4.1.2 on 2022-11-04 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_chat_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
