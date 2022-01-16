from django.db import models, migrations
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.syndication.views import Feed
from datetime import datetime
from group.models import Group
from member.models import Person, SoilTag, PlantTag

# Create your models here.


class Feed(models.Model):
    class Meta:
        db_table = 'Feed'
    Title = models.CharField(max_length=255)
    Message = models.CharField(max_length=255)
    Photo = models.ImageField(upload_to ='uploads/', blank=True,null=True, default="")
    Video = models.FileField(upload_to='uploads/', blank=True, null=True, default="")
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    Group = models.ForeignKey(Group, on_delete=models.CASCADE)
    Creator = models.ForeignKey(Person, on_delete=models.CASCADE)


    def save(self):
        super().save()
        super().save(using='farming')
        return self.id

    def deleteRecordFarming(self):
        super().delete(using='farming')
        
    def deleteRecordIgrow(self):
        super().delete()
    

class Comment(models.Model):
    class Meta:
        db_table = 'Comment'    
    Message = models.TextField()
    Pictures = models.ImageField(upload_to='uploads/', null=True)
    Video = models.FileField(upload_to='uploads/', null=True)
    Feed = models.ForeignKey(Feed, related_name="comments", on_delete=models.CASCADE)
    Commenter = models.ForeignKey(Person, on_delete=models.CASCADE)

    def save(self):
        super().save()
        super().save(using='farming')
        return self.id

    def deleteRecordFarming(self):
        super().delete(using='farming')
        
    def deleteRecordIgrow(self):
        super().delete()


class FeedSoilTagging(models.Model):

    FeedSoilTag = models.ForeignKey(Feed, related_name="soilTagging", on_delete=models.CASCADE)    
    soilTag = models.ForeignKey(SoilTag, on_delete=models.CASCADE)
    
    class Meta:  
        unique_together = [['FeedSoilTag', 'soilTag']]

    def save(self):
        super().save()
        super().save(using='farming')
   
    def deleteRecordFarming(self):
        super().delete(using='farming')
        
    def deleteRecordIgrow(self):
        super().delete()


class FeedPlantTagging(models.Model):

    FeedPlantTag = models.ForeignKey(Feed, related_name="plantTagging", on_delete=models.CASCADE)    
    plantTag = models.ForeignKey(PlantTag, on_delete=models.CASCADE)
   
    class Meta:  
        unique_together = [['FeedPlantTag', 'plantTag']]

    def save(self):
        super().save()
        super().save(using='farming')
   
    def deleteRecordFarming(self):
        super().delete(using='farming')
        
    def deleteRecordIgrow(self):
        super().delete()

