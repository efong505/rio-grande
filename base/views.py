from itertools import count
from django.forms import SlugField
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import About, Post, Category 
from django.db.models import Q
from django.db.models import Count
from .forms import CommentForm
from next_prev import next_in_order, prev_in_order
from .forms import PostForm
from django.contrib.auth.decorators import login_required



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    # rooms = Room.objects.all()
    categories = Category.objects.all()[0:3]
    #post_slug = Post.objects.get(slug=slug)
    posts = Post.objects.all()[0:3]
    
    context = {'categories':categories, 
               'posts':posts}
    return render(request, 'base/home.html', context)

# Original allposts before pagination
# def allposts(request):
#     posts = Post.objects.order_by('-created_on')
#     categories = Category.objects.all().annotate(posts_count = Count('posts'))    
#     context = {'posts':posts, 'categories':categories}
#     return render(request, 'base/blogMain.html', context)

#allposts for pagination
def allposts(request):
    search_post = request.GET.get('search')
    if search_post:
        posts = Post.objects.filter(Q(title__icontains=search_post) | Q(content__icontains=search_post))
    else:
        posts = Post.objects.order_by('-created_on')
    #posts = Post.objects.order_by('-created_on')
    categories = Category.objects.all().annotate(posts_count = Count('posts'))    
    page_num = request.GET.get('page', 1)
    paginator = Paginator(posts, 3)
    try: 
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    context = {'posts':posts, 'categories':categories, 'page_obj':page_obj}
    return render(request, 'base/blogMain.html', context)

def posts_crud(request):
    if request.user.is_superuser:    
        posts = Post.objects.order_by('-created_on')
        context = {'posts':posts}
        return render(request, 'base/posts.html', context)
    else:
        return redirect('home')

def category_post_list(request, slug):
    category = Category.objects.get(slug=slug)
    
    search_post = request.GET.get('search')
    if search_post:
        posts = Post.objects.filter(category=category).filter(Q(title__icontains=search_post) | Q(content__icontains=search_post))
    else:
        posts = Post.objects.filter(category=category)
    #posts = Post.objects.filter(category=category)
    
    categories = Category.objects.all().annotate(posts_count= Count('posts'))
    context = {'posts':posts, 'categories':categories,  'category':category}
    return render(request, 'base/category.html', context)



def post(request, slug):
    post = Post.objects.get(slug=slug)
    
    post_comment = get_object_or_404(Post, slug=slug)
    # search_post = request.GET.get('search')
    # if search_post:
    #     posts = Post.objects.filter(Q(title__icontains=search_post) | Q(content__icontains=search_post))
    # else:
    #     posts = Post.objects.order_by('-created_on')
    posts = Post.objects.order_by('-created_on')
    comments = post_comment.comments.filter(active=True)
    new_comment = None
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post_comment
            new_comment.save()
    else:
        comment_form = CommentForm()
        
    # next and previous 
    next = next_in_order(post)
    prev = prev_in_order(post)
    
    # second newest and oldest
    qs = Post.objects.all().order_by('-created_on')
    newest = qs.first()
    second_newest = next_in_order(newest, qs=qs)
    oldest = prev_in_order(newest, qs=qs, loop=True)
    
    categories = Category.objects.all().annotate(posts_count = Count('posts'))
    context = { 'post':post, 'posts':posts, 'categories':categories, 'second_newest':second_newest, 
                'oldest':oldest,  'next':next, 'prev':prev,
                'comments':comments, 'new_comment':new_comment, 'comment_form': comment_form}
    return render(request, 'base/post_detail.html', context)


def about(request):
    title = About.objects.all()
    story = About.objects.all()
    posts = Post.objects.all()
    context = {'title':title, 'story': story, 'posts':posts}
    return render(request, 'about.html', context)

@login_required(login_url='login')
def createPost(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts-list')
    context = {'form':form}
    return render(request, 'base/post_form.html', context)

@login_required(login_url='login')
def updatePost(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts-list')
    context = {'form':form}
    return render(request, 'base/post_form.html', context)

@login_required(login_url='login')
def deletePost(request, slug):
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        post.delete()
        return redirect('posts-list')
    context = {'object':post}
    return render(request, 'base/delete_template.html', context)