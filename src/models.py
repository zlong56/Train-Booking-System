from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.db.models.deletion import CASCADE, DO_NOTHING, SET_NULL
from django.db.models.fields import BooleanField, CharField, DateTimeCheckMixin
from core.settings import STATIC_ROOT
from django.core.files.storage import default_storage
import os 
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime

class MyAccountManager(BaseUserManager):
    def create_user(self, Username, password, Name):
        if not Username:
            raise ValueError["Users must have a username"]
        if not password:
            raise ValueError["Users must have a password"]
        
        user = self.model(
            Username = Username,
            Name = Name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Username, password, Name):
        user = self.create_user(
            Username = Username,
            password = password,
            Name = Name
        )
        user.is_staff=True
        user.is_admin=True
        user.is_superuser=True
        user.is_active=True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    Key = models.CharField(max_length=100, blank=True, null=True)
    DateCreated = models.DateTimeField(auto_now_add=True, null=True)
    AccType = models.CharField(max_length=50, blank=True, null=True)
    Username = models.CharField(max_length=100, unique=True)
    Name = models.CharField(max_length=100, blank=False)
    IC = models.CharField(max_length=12, blank=True, null=True)
    PhoneNumber = models.CharField(max_length=100, blank=True, null=True)
    Email = models.CharField(max_length=50, blank=True, null=True)
    ProfilePic = models.ImageField(default='/assets/images/users/user-dummy-img.jpg')
    
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    is_active = models.BooleanField(default=False)
    RawPassword = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = 'Username'
    REQUIRED_FIELDS = ['Name',]

    objects = MyAccountManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Admin(Account):
    pass

class Client(Account):
    pass

class State(models.Model):
    Name = models.CharField(max_length=100, blank=True, null=True)
    
class Station(models.Model):
    DateCreated = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    Name = models.CharField(max_length=50, blank=True, null=True)
    State = models.ForeignKey(State, on_delete=CASCADE, blank=True, null=True)
    StationCode = models.CharField(max_length=20, blank=True, null=True)
    
class Train(models.Model):
    DateCreated = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    TrainCode = models.CharField(max_length=20, blank=True, null=True)
    DepartDateTime = models.DateTimeField(blank=True, null=True)
    ArriveDateTime = models.DateTimeField(blank=True, null=True)
    TotalPassenger = models.CharField(max_length=3, blank=True, null=True)
    Price = models.CharField(max_length=10, blank=True, null=True)
    is_complete = BooleanField(default=False)
    
    DepartState = models.CharField(max_length=50, blank=True, null=True)
    ArriveState = models.CharField(max_length=50, blank=True, null=True)
    DepartLocation = models.ForeignKey(Station, related_name='depart', on_delete=models.CASCADE, blank=True, null=True)
    ArriveLocation = models.ForeignKey(Station, related_name='arrive', on_delete=models.CASCADE, blank=True, null=True)
    
class Coach(models.Model):
    CODE_CHOICE = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
    ]
    
    DateCreated = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    CoachType = models.CharField(max_length=5, blank=True, null=True, choices=CODE_CHOICE)
    
    Train = models.ForeignKey(Train, on_delete=models.CASCADE, blank=True, null=True)

class Seat(models.Model):
    SEAT_STATUS = [
        ('RESERVED', 'RESERVED'),
        ('LOCKED', 'LOCKED'),
        ('AVAILABLE', 'AVAILABLE')
    ]
    
    DateCreated = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    CoachType = models.CharField(max_length=2, blank=True, null=True)
    SeatNo = models.CharField(max_length=5, blank=True, null=True)
    SeatStatus = models.CharField(max_length=50, blank=True, null=True, choices=SEAT_STATUS, default='AVAILABLE')
    last_lock_time = models.DateTimeField(blank=True, null=True)
    is_locked = models.BooleanField(default=False)
    
    Coach = models.ForeignKey(Coach, on_delete=models.CASCADE, blank=True, null=True)
    Train = models.ForeignKey(Train, on_delete=models.CASCADE, blank=True, null=True)
    
class Booking(models.Model):
    BOOKING_STATUS = [
        ('PENDING PAYMENT', 'PENDING PAYMENT'),
        ('SUCCESS', 'SUCCESS'),
        ('CANCEL', 'CANCEL')
    ]
    
    DateCreated = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    BookingStatus = models.CharField(max_length=100, blank=True, null=True, choices=BOOKING_STATUS)
    Price = models.CharField(max_length=10, blank=True, null=True)
    BookingNo = models.CharField(max_length=20, blank=True, null=True)
    NoPax = models.IntegerField(blank=True, null=True)
    
    Client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    Train = models.ForeignKey(Train, on_delete=models.CASCADE, blank=True, null=True)
    Coach = models.ForeignKey(Coach, on_delete=models.CASCADE, blank=True, null=True)
    Seat = models.ManyToManyField(Seat, blank=True, related_name='Client_Seats')
