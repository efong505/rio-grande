from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('posts/', views.posts_crud, name="posts-list"),
    # path('blog/', views.PostList.as_view(), name="blog"),
    # path('blog/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('blog/', views.allposts, name="blog"),
    path('blog/<slug:slug>/', views.post, name="post"),
    path('blog/category/<slug:slug>/',views.category_post_list, name="category"),
    # path('blog/category/<slug:slug>/', views.Category, name='category'),
    path('summernote/', include('django_summernote.urls')),
    path('blog/category/', views.category_post_list, name='categories'),
    
    # path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('about/', views.about, name="about"),
    path('create-post/', views.createPost, name="create-post"),
    # path('categories/',views.categories_page, name="categories_page"),
    path('update-post/<slug:slug>/', views.updatePost, name="update-post"),
    path('delete-post/<slug:slug>/', views.deletePost, name="delete-post"),
    
    
    
   # path('room/<str:pk>/', views.room, name="room"),
]

    
# X_FRAME_OPTIONS = 'SAMEORIGIN'

