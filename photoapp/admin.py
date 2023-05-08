from django.contrib import admin

# Register your models here.
from .models import Photo, FollowerCount

admin.site.register(Photo)
