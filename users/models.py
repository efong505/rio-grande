from re import T
from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import uuid



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    created = models.DateTimeField(auto_now_add=True)
    #id=models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    def __str__(self):
        return str(self.username)
    
