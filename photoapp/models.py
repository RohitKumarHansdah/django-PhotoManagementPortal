from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
# from django.contrib.auth.models import Submitter


# Create your models here.

class Photo(models.Model):

    title = models.CharField(max_length=45)
    description = models.CharField(max_length=250) 
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='photos/')
    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tags = TaggableManager() 

    def __str__(self):
        return self.title

class Like(models.Model):

    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')

    def __str__(self):
        return self.image
    
class Follow(models.Model):

    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    follows = models.ManyToManyField(get_user_model(), related_name='followed_by')

    def __str__(self):
        return self.submitter
    

class FollowerCount(models.Model):
    follower = models.CharField(max_length=1000)
    submitter = models.CharField(max_length=1000)

    def __str__(self):
        return self.submitter
    