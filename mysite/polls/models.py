from django.db import models
import datetime
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class users(models.Model):
    name = models.CharField(max_length=30)
    roll_no = models.IntegerField(primary_key=True)
    mobile_no = models.CharField(max_length=10)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=12)
    hostel = models.IntegerField(validators=[MaxValueValidator(13), MinValueValidator(1)])
    room_no = models.IntegerField(validators=[MaxValueValidator(900), MinValueValidator(100)])

class cycles(models.Model):
    roll_no = models.ForeignKey(users, on_delete=models.CASCADE)
    cycle_brand = models.CharField(max_length=20,default="none")
    cycle_type = models.CharField(max_length=10,default="none")
    cycle_description = models.CharField(max_length=100,default="none")
    available = models.IntegerField(validators=[MaxValueValidator(2), MinValueValidator(0)],default=0)

class session(models.Model):
    session_id = models.CharField(max_length=100)
    roll_no = models.IntegerField(primary_key=True)

class cycleRequests(models.Model):
    taker=models.IntegerField()
    cycle=models.IntegerField()
    status = models.IntegerField(default=0)

# name = "abc",roll_no = "123",mobile_no = "9151515151",email = "a@b.com",password = "abc",hostel = "2",room_no = "111"    	