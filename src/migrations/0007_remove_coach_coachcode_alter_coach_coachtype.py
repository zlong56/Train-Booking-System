# Generated by Django 5.0.7 on 2024-11-22 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0006_remove_train_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coach',
            name='CoachCode',
        ),
        migrations.AlterField(
            model_name='coach',
            name='CoachType',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F')], max_length=5, null=True),
        ),
    ]
