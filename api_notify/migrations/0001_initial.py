# Generated by Django 5.2.1 on 2025-05-14 22:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1024, verbose_name='Текст сообщения')),
            ],
        ),
        migrations.CreateModel(
            name='LogMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daytime_send', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время отправки')),
                ('recepient', models.CharField(blank=True, max_length=150, null=True, verbose_name='Получатель')),
                ('status', models.CharField(blank=True, choices=[('N', 'Не отправлено'), ('S', 'Отправлено')], default='N', max_length=13, null=True, verbose_name='Статус отправки')),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_notify.message', verbose_name='Текст сообщения')),
            ],
        ),
    ]
