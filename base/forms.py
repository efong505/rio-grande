from .models import Comment, Post
from django import forms
from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        
        # fields = [
        #     'tags',
        # ]
        # fields = '__all__'
        fields = ['category', 'title', 
                  'slug', 'author', 'image', 
                  'tags', 'intro','content', 'status', 'featured']
        foo = forms.CharField(widget=SummernoteWidget())
        # widgets = {
        #     'tags':forms.CheckboxSelectMultiple(),
        # }
        widgets = {
            'content': SummernoteWidget(),
            'tags':forms.CheckboxSelectMultiple(),
            #'content': SummernoteInplaceWidget(),
        }
        def __init__(self, *agrs, **kwargs):
            super(PostForm, self).__init__()
            for name,field in self.fields.items():
                field.widget.attrs.update({'class':'input'})
            self.fields['title'].widget.attrs.update({'class':'input', 'placeholder':'Add Title'})
        