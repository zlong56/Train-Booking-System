# Generated by Django 5.0.7 on 2024-11-21 13:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('Key', models.CharField(blank=True, max_length=100, null=True)),
                ('DateCreated', models.DateTimeField(auto_now_add=True, null=True)),
                ('AccType', models.CharField(blank=True, max_length=50, null=True)),
                ('Username', models.CharField(max_length=100, unique=True)),
                ('Name', models.CharField(max_length=100)),
                ('IC', models.CharField(blank=True, max_length=12, null=True)),
                ('PhoneNumber', models.CharField(blank=True, max_length=100, null=True)),
                ('Email', models.CharField(blank=True, max_length=50, null=True)),
                ('ProfilePic', models.ImageField(default='/assets/images/users/user-dummy-img.jpg', upload_to='')),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('RawPassword', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DateCreated', models.DateTimeField(auto_now_add=True, null=True)),
                ('CoachCode', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F')], max_length=5, null=True)),
                ('CoachType', models.CharField(blank=True, max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SavedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DateCreated', models.DateTimeField(auto_now_add=True)),
                ('File', models.FileField(upload_to='saved_file/')),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DateCreated', models.DateTimeField(auto_now_add=True, null=True)),
                ('Location', models.CharField(blank=True, max_length=50, null=True)),
                ('StationCode', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('account_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('src.account',),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('account_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('src.account',),
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DateCreated', models.DateTimeField(auto_now_add=True, null=True)),
                ('SeatNo', models.CharField(blank=True, max_length=5, null=True)),
                ('SeatStatus', models.CharField(blank=True, choices=[('LOCKED', 'LOCKED'), ('AVAILABLE', 'AVAILABLE')], default='AVAILABLE', max_length=50, null=True)),
                ('LockTime', models.DateTimeField(blank=True, null=True)),
                ('is_locked', models.BooleanField(default=False)),
                ('Coach', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='src.coach')),
            ],
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DateCreated', models.DateTimeField(auto_now_add=True, null=True)),
                ('TrainCode', models.CharField(blank=True, max_length=20, null=True)),
                ('DepartDateTime', models.DateTimeField(blank=True, null=True)),
                ('ArriveDateTime', models.DateTimeField(blank=True, null=True)),
                ('TotalPassenger', models.CharField(blank=True, max_length=3, null=True)),
                ('Price', models.CharField(blank=True, max_length=10, null=True)),
                ('is_complete', models.BooleanField(default=False)),
                ('ArriveLocation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arrive', to='src.station')),
                ('DepartLocation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='depart', to='src.station')),
            ],
        ),
        migrations.AddField(
            model_name='coach',
            name='Train',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='src.train'),
        ),
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DateCreated', models.DateTimeField(auto_now_add=True)),
                ('FileName', models.CharField(max_length=255)),
                ('SavedFileName', models.CharField(max_length=255)),
                ('File', models.FileField(upload_to='temp/')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DateCreated', models.DateTimeField(auto_now_add=True)),
                ('Activity', models.CharField(max_length=500)),
                ('Link', models.CharField(blank=True, max_length=500, null=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DateCreated', models.DateTimeField(auto_now_add=True, null=True)),
                ('BookingStatus', models.CharField(blank=True, choices=[('PROCESSING', 'PROCESSING'), ('SUCCESS', 'SUCCESS'), ('FAIL', 'FAIL')], max_length=100, null=True)),
                ('Price', models.CharField(blank=True, max_length=10, null=True)),
                ('BookingNo', models.CharField(blank=True, max_length=20, null=True)),
                ('Coach', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='src.coach')),
                ('Seat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='src.seat')),
                ('Train', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='src.train')),
                ('Client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='src.client')),
            ],
        ),
    ]