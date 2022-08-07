from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from base.models import About
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 
                  'password2']
        labels = {
            'first_name':'Name',
        }
    
    def __init__(self, *agrs, **kwargs):
        super(CustomUserCreationForm, self).__init__(*agrs, **kwargs)
        
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
            
class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields ='__all__'
        foo = forms.CharField(widget=SummernoteWidget())
        #fields = ['title']
        widgets = {
            'story':SummernoteWidget(),
        }