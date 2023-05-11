from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager


# Create your models here.
class Photo(models.Model):

    title = models.CharField(max_length=45)
    description = models.CharField(max_length=250) 
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='photos/')
    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tags = TaggableManager()
    # likes = models.ManyToManyField(get_user_model(), related_name='liked_photos', blank=True)

    def __str__(self):
        return self.title

'''Like and Follow Models'''
class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

class Follow(models.Model):
    follower = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='followers')

    


    