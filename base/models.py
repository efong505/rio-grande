from distutils.text_file import TextFile
from statistics import mode
from tkinter import CASCADE
from unicodedata import category
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.forms import CharField, DateTimeField


# from base.views import Category


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    thumbnail = models.ImageField(null=True,blank=True)
    # parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    class Meta:
        # unique_together = ('slug', 'parent')
        verbose_name_plural = "categories"
    def __str__(self):
        return self.title

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts")
    slug = models.SlugField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True,
                                       default="default.jpg")
    tags = models.ManyToManyField('Tag', blank=True)
    title = models.CharField(max_length=200, unique=True)
    intro = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    #thumbnail = models.ImageField()
    # categories = models.ManyToManyField(Category, null=True)
    featured = models.BooleanField()
    
    class Meta:
        ordering = ['-created_on']
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['created_on']
    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
    
    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()
    
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
   
   
# class Reply(models.Model):
#     comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
#     name = models.ForeignKey(Comment, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     reply = models.TextField()
    
#     def __str__(self):
#         return self.name
    
#     @property
#     def get_replies(self):
#         return self.replies.all()

class About(models.Model):
    title = models.CharField(max_length=200)
    story = models.TextField()
    image = models.ImageField(null=True, blank=True,
                                       default="default.jpg")
    
    class Meta:
        verbose_name_plural = "About Options"
    def __str__(self):
        return self.title
    
    
class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    def __str__(self):
        return self.name
    
# class Topic(models.Model):
#     name = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name

# class Room(models.Model):
#     host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
#     name = models.CharField(max_length=200)
#     description = models.TextField(null=True, blank=True)
#     #participants = 
#     update = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


# class Message(models.Model):
#     user = models.ForeignKey(User, on_delete=CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     body = models.TextField()
#     update = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.body[0:50]
