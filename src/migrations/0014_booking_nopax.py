# Generated by Django 5.0.7 on 2024-11-25 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0013_alter_booking_bookingstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='NoPax',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
