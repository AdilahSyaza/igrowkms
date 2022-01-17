from django.db import models, migrations
# from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.syndication.views import Feed
from member.models import Person, SoilTag, PlantTag

# Create your models here.

class Group(models.Model):
    
    Name = models.CharField(max_length=150)
    About = models.CharField(max_length=1000)
    Media = models.ImageField(upload_to='uploads/',default="")
    Username = models.ForeignKey(Person, on_delete=models.CASCADE)


    def save(self):
        # group = self
        super().save()
        super().save(using='farming')
        # return group
        return self.id
    
    def deleteRecordFarming(self):
        super().delete(using='farming')
        
    def deleteRecordIgrow(self):
        super().delete()
    
    class Meta:
        db_table = 'group'


class GroupMembership(models.Model):
    
    GroupName = models.ForeignKey(Group, on_delete=models.CASCADE)
    GroupMember = models.ForeignKey(Person, on_delete=models.CASCADE)
    # joined_on = models.DateTimeField(default=datetime.now, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True, blank=True)

    def save(self):
        super().save()
        super().save(using='farming')

    
    class Meta:
        
        unique_together = [['GroupName', 'GroupMember']]


class GroupSoilTagging(models.Model):

    GroupSoilTag = models.ForeignKey(Group, related_name="soilTagging", on_delete=models.CASCADE)    
    soilTag = models.ForeignKey(SoilTag, on_delete=models.CASCADE)
   
    class Meta:  
        unique_together = [['GroupSoilTag', 'soilTag']]

    def save(self):
        super().save()
        super().save(using='farming')
   
    def deleteRecordFarming(self):
        super().delete(using='farming')
        
    def deleteRecordIgrow(self):
        super().delete()


class GroupPlantTagging(models.Model):

    GroupPlantTag = models.ForeignKey(Group, related_name="plantTagging", on_delete=models.CASCADE)    
    plantTag = models.ForeignKey(PlantTag, on_delete=models.CASCADE)
   
    class Meta:  
        unique_together = [['GroupPlantTag', 'plantTag']]

    def save(self):
        super().save()
        super().save(using='farming')
   
    def deleteRecordFarming(self):
        super().delete(using='farming')
        
    def deleteRecordIgrow(self):
        super().delete()

