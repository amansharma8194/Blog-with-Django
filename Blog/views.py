from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .forms import *
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    form = BlogForm()
    if request.method=='POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            desc = form.cleaned_data['desc']
            user_id = request.user.id
            obj = Blog(title=title,desc=desc,user_id=user_id)
            obj.save()
            return redirect(reverse('home_page'))
        else:
            messages.success(request, form.errors)
    data = Blog.objects.all().order_by('-created_at')[:5]
    context = {'form': form, 'data': data}
    return render(request, 'Blog/index.html', context)

def viewBlog(request, id):
    data = Blog.objects.get(id=id)
    should_modify = True if data.user_id==request.user.id else False
    commentForm = CommentForm()
    commentsData = Comment.objects.filter(blog_id=id).order_by('-created_at')
    if request.method=='POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comm']
            obj = Comment(comm = comment ,username = request.user.username, blog_id = id, user_id = request.user.id)
            obj.save()
            return redirect(reverse('blog_page', args=[id]))
    context = {'data': data, 'commentForm': commentForm, 'commentsData': commentsData, 'should_modify': should_modify}
    return render(request, 'Blog/blog.html', context)

@login_required(login_url=reverse_lazy('accounts:login_page'))
def editBlog(request, id):
    data = Blog.objects.get(id=id)
    form = BlogForm(instance = data)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance = data)
        if form.is_valid():
            form.save()
            return redirect(reverse('blog_page', args=[id]))
        else:
            messages.success(request, form.errors)
    context = {'form': form}
    return render(request, 'Blog/editBlog.html', context)


@login_required(login_url=reverse_lazy('accounts:login_page'))
def deleteBlog(request, id):
    Blog.objects.get(id=id).delete()
    return redirect(reverse('home_page'))

def allBlog(request):
    data = Blog.objects.all().order_by('-created_at')
    pagin = Paginator(data, 4)
    page = request.GET.get('page')
    data = pagin.get_page(page)
    context = {'data': data}
    return render(request, 'Blog/allblogs.html', context)


def view_profile(request, id):
    userData = User.objects.get(id=id)
    blogData = Blog.objects.filter(user_id=id).order_by('-created_at')
    context = {'userData': userData, 'blogData': blogData}
    return render(request, 'BLog/profile.html', context)