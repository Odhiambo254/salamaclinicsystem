# Generated by Django 5.1.3 on 2024-12-01 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salama', '0005_remove_patient_email_patient_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='id_number',
            field=models.IntegerField(max_length=11, null=True, unique=True),
        ),
    ]
