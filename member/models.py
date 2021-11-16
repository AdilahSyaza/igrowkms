from django.db import models, migrations
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils import timezone
from django.conf import settings

class Person(models.Model):
    
    Email = models.CharField(max_length=150)
    # Pwd = models.CharField(max_length=150)
    Password = models.CharField(max_length=150)
    Username = models.CharField(max_length=150)
    Name = models.CharField(max_length=150)
    DateOfBirth = models.CharField(max_length=150)
    Age = models.IntegerField ()
    District = models.CharField(max_length=150)
    State = models.CharField(max_length=150)
    Occupation = models.CharField(max_length=150)
    About = models.CharField(max_length=150)
    Gender = models.CharField(max_length=1)
    MaritalStatus = models.CharField(max_length=150)
    UserLevel = models.CharField(max_length=150)

    def save(self):
        super().save()
        super().save(using='farming')

    class Meta:
        db_table = 'login_person'

def user_form(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)
        instance.Person.save()

class Member(models.Model):
    class Meta:
        db_table = 'Member'
    Name = models.CharField(max_length=150, blank=True)
    Study = models.CharField(max_length=1000, blank=True)
    Lives = models.CharField(max_length=1000, blank=True)
    # cuba
    # friends = models.ManyToManyField("Person", blank=True)
    

# cuba
class FriendRequest(models.Model):
	to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
	from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "From {}, to {}".format(self.from_user.username, self.to_user.username)


class SensorData(models.Model):
    class Meta:
        db_table = 'SensorData'    
    Detail = models.CharField(max_length=255)
    Name = models.CharField(max_length=150)

class Plants(models.Model):
    class Meta:
        db_table = 'Plants'
    Pictures = models.ImageField(upload_to='uploads/')
    Species = models.CharField(max_length=150)
    Types = models.CharField(max_length=150)


class Users(models.Model):
    username = models.CharField(max_length=10, unique=True) #AI190201
    password = models.CharField(max_length=30) #ninja saga
    name = models.CharField(max_length=100) #FAIZ BIN AB. HAMID
    age = models.IntegerField() #22
    ranking = models.FloatField() #2.5

    def upload_photo(self, filename):
        path = 'LOGIN/photo/{}'.format(filename)
        return path

    photo = models.ImageField(upload_to=upload_photo, null=True, blank=True)

    def upload_file(self, filename):
        path = 'LOGIN/file/{}'.format(filename)
        return path

    resume = models.ImageField(upload_to=upload_file, null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.password}"