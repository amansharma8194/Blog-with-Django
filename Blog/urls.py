from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home_page'), 
    path('blog/<int:id>', viewBlog, name='blog_page'), 
    path('edit/<int:id>', editBlog, name='edit_blog_page'),
    path('delete/<int:id>', deleteBlog, name='delete_blog_page'), 
    path('allblogs/', allBlog, name='all_blogs_page'),
    path('profile/<int:id>', view_profile, name='profile_page'),
]
