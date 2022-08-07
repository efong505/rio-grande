from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import About, Post, Category, Comment, Tag

#admin.site.register(Post)
# Register your models here.

class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)
    
class AboutAdmin(SummernoteModelAdmin):
    list_display = ('title',)
    search_fields = ['title', 'story']
    summernote_fields = ('story',)
    
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'slug', 'status','created_on')
#     list_filter = ("status",)
#     search_fields = ['title', 'content']
#     prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ['title','slug']
    prepopulated_fields = {'slug': ('title',)}
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(active=True)

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(Tag)

#from .models import #, Topic, Message

# admin.site.register(Room)
# admin.site.register(Topic)
# admin.site.register(Message)