# Generated by Django 5.0.7 on 2024-11-24 14:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0008_train_arrivestate_train_departstate'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='Train',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='src.train'),
        ),
    ]