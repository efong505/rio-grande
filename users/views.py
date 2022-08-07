from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from base.models import About, Post

from .models import Profile
#from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, AboutForm

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User name does not exist') 
            return redirect('home') 
            
        user = authenticate(request, username=username, password=password)      
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
           
        else:
            messages.error(request, 'Username OR password is incorrect')
            return redirect('home') 
    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.warning(request, 'User was logged out')
    return redirect('home')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
             user = form.save(commit=False)
             user.username = user.username.lower()
             user.save()
             
             messages.success(request, 'User account was created!')
             login(request, user)
             return redirect('home')
        else:
             messages.error(
                 request, 'An error has occured during registration!')
             
    context = {'page':page, 'form':form}
    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles = Profile.objects.all()
    context = { 'profiles':profiles }
    return render(request,'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {'profile':profile}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')    
def adminAccount(request):
    if request.user.is_superuser:
        profile = request.user.profile
        title = About.objects.all()
        story = About.objects.all()
        posts = Post.objects.all()
        context = {'title':title, 'story':story,'posts':posts, 'profile':profile}
        return render(request,'users/account.html', context)
    else: 
        return redirect('home')
    
@login_required(login_url='login')
def editAdminAccount(request):
    if request.user.is_superuser:
        about = About.objects.get(pk=1)
        form = AboutForm(instance=about)
        
        if request.method == 'POST':
            form = AboutForm(request.POST, request.FILES, instance=about)
            if form.is_valid():
                form.save()
                return redirect('account')
                
        context = {'form':form}
        return render(request, 'users/profile_form.html',context) 