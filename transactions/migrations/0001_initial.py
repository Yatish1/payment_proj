# Generated by Django 4.2.4 on 2023-10-28 06:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bankaccounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=15, max_length=20, prefix='TRN', unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('status', models.CharField(choices=[['failed', 'FAILED'], ['completed', 'COMPLETED'], ['pending', 'PENDING'], ['processing', 'PROCESSING'], ['request_sent', 'REQUEST_SENT'], ['request_processing', 'REQUEST_PROCESSING']], default='pending', max_length=100)),
                ('transaction_type', models.CharField(choices=[['transfer', 'TRANSFER'], ['withdraw', 'WITHDRAW'], ['refund', 'REFUND'], ['received', 'RECEIVED'], ['request', 'REQUEST'], ['none', 'NONE']], default='none', max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('receiver_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receiver_account', to='bankaccounts.account')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender', to=settings.AUTH_USER_MODEL)),
                ('sender_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender_account', to='bankaccounts.account')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=10, max_length=20, prefix='CRED', unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('name', models.CharField(max_length=255)),
                ('number', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=16, max_length=16, prefix='', unique=True)),
                ('month', models.CharField(max_length=15)),
                ('year', models.IntegerField()),
                ('cvv', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=3, max_length=6, prefix='', unique=True)),
                ('card_type', models.CharField(choices=[['master_card', 'MASTER_CARD'], ['visa', 'VISA'], ['rupay', 'RUPAY'], ['platinum', 'PLATINUM']], max_length=20)),
                ('card_status', models.CharField(choices=[['active', 'ACTIVE'], ['in_active', 'IN_ACTIVE']], default='in_active', max_length=20)),
                ('date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
