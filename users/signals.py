from logging import StrFormatStyle
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User

from base.models import About
from .models import Profile 

# @receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    print('Profile Signal Trigger!')
    # print('Profile Saved!')
    # print('Instance:', instance)
    # print('CREATED:', created)
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user, 
            username=user.username,
            email=user.email,
            name=user.first_name
        )
       
def createAdminUser(sender, instance, created, **kwargs):
    if created:
        title = instance
        about = About.objects.create(
            title=title,
            story=title.story,
            image=title.image,
        )
        
# def updateUser(sender, instance, created, **kwargs):
#     about = instance
#     title = about.title
#     if created == False:
#         title.title = about.title
#         title.story = about.story
#         title.image = about.image
#         title.save()
    
    
    
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()
     
    
post_save.connect(createProfile, sender=User)
# post_save.connect(updateUser, sender=About)
post_save.connect(createAdminUser, sender=About)
post_delete.connect(deleteUser, sender=Profile)