# Generated by Django 4.2.4 on 2023-10-12 06:30

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0010_alter_creditcard_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='number',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=16, max_length=16, prefix='', unique=True),
        ),
    ]
