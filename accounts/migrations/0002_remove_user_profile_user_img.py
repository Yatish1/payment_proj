# Generated by Django 4.2.4 on 2023-09-01 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_profile',
            name='user_img',
        ),
    ]
