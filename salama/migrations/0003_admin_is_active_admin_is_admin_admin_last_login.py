# Generated by Django 5.1.3 on 2024-11-30 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salama', '0002_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='admin',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='admin',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]
