from django.db import models, migrations
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.syndication.views import Feed

# Create your models here.

class Workshop(models.Model):
    class Meta:
        db_table = 'Workshop'
    ProgrammeName = models.CharField(max_length=150,default="")
    Description=models.CharField(max_length=150,default="")
    Date = models.DateField()
    Session = models.CharField(max_length=150)

    def save(self):
        super().save()
        super().save(using='farming')


class Booking(models.Model):
    class Meta:
        db_table = 'Booking'
    Name = models.CharField(max_length=150)
    ProgrammeName = models.CharField(max_length=150,default="")
    Date = models.DateField()
    Session = models.CharField(max_length=150)

    def save(self):
        super().save()
        super().save(using='farming')

