# Generated by Django 5.0.7 on 2024-11-25 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0012_delete_savedfile_remove_useractivity_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='BookingStatus',
            field=models.CharField(blank=True, choices=[('PENDING PAYMENT', 'PENDING PAYMENT'), ('SUCCESS', 'SUCCESS'), ('CANCEL', 'CANCEL')], max_length=100, null=True),
        ),
    ]
