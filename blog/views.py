from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import generics
from .models import *
from .serializers import *
from .forms import *
import pygal

def main(req):
    return render(req,'blog/main.html',{})

def login(req):
    return render(req,'blog/login.html',{'form':loginForm()})

def logout(req):
    logout(req)

def new_user(req):
    if req.POST:
        form = UserCreationForm(req.POST)
        form.fields['password1'].widget.attrs['class'] = 'form-control'
        form.fields['password2'].widget.attrs['class'] = 'form-control'
        form.fields['username'].widget.attrs['class'] = 'form-control'
        if form.is_valid():
            form.save()
            newUser = auth.authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
            auth.login(req,newUser)
            return redirect('blog.views.new_profile')
    else:
        form = UserCreationForm()
        form.fields['password1'].widget.attrs['class'] = 'form-control'
        form.fields['password2'].widget.attrs['class'] = 'form-control'
        form.fields['username'].widget.attrs['class'] = 'form-control'

    return render(req,'blog/new_user.html',{'form':form})

@login_required(login_url='/login/')
def profile_redirect(req):
    return redirect(req.user.username+'/')

# @login_required(login_url='/login/')
def profile(req,name, num= 1):
    user = auth.models.User.objects.get(username=name)
    my_profile = Profile.objects.get(user=user)
    my_posts = Post.objects.filter(author=user)
    posts = Paginator(my_posts, 5)
    is_my_profile = user.username == req.user.username

    if req.method == 'POST':
        form = PostForm(req.POST)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.author = req.user
            profile.save()
            return redirect('/profile/{}/'.format(user.username))
    else:
        form = PostForm()

    return render(req,'blog/profile.html',{
                    'post_list':posts.page(num),
                    'profile':my_profile,
                    'new_post_form':form,
                    'current_user':user,
                    'is_my_profile':is_my_profile})

@login_required(login_url='/login/')
def new_post(req):
    if req.method == 'POST':
        form = PostForm(req.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = req.user
            post.save()
            return redirect('blog.views.profile')
    else:
        form = PostForm()
    return render(req,'blog/new_post.html',{'new_post_form':form})

@login_required(login_url='/login/')
def new_profile(req):
    if req.method == 'POST':
        form = ProfileForm(req.POST,req.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            post.user = req.user
            post.save()
            return redirect('/profile/{}/'.format(req.user.username))
    else:
        form = ProfileForm()
    return render(req,'blog/new_profile.html',{'form':form})

@login_required(login_url='/login/')
def post(req,num):
    p = Post.objects.get(id=num)
    comments = Comment.objects.filter(post=p)
    my_profile = Profile.objects.get(user=req.user)
    likes = Like.objects.filter(post=p)
    if req.method == 'POST':
        form = CommentForm(req.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.author = req.user
            comment.post = Post.objects.get(id=num)
            comment.save()
            return render(req,'blog/post.html',{'post':p,'profile':my_profile,'comments':comments,'comment_form':CommentForm()})
    else:
        form = CommentForm()

    return render(req,'blog/post.html',{'post':p,'profile':my_profile,'comments':comments,'comment_form':form,'likes':likes})

@login_required(login_url='/login/')
def like_post(req,num):
    this_post = Post.objects.get(id=num)
    like = Like.objects.filter(user=req.user,post=this_post)
    if like:
        like.delete()
    else:
        like = Like(post=this_post,user=req.user)
        like.save()
    return redirect('/post/'+num+'/')


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer




@login_required(login_url='/login/')
def statistics(req):
    bc = pygal.Pie().add('Мужчины', 30).add('Женщины', 70)
    bc.title = "Посещаемоть"

    line_chart = pygal.Bar()
    line_chart.title = 'Посещаемость за последниее время'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('женщины', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('мужчины',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    line_chart.add('люди старше ', [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('дети',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])

    from datetime import time
    dateline = pygal.TimeLine(x_label_rotation=25)
    dateline.add("Активность", [
      (time(), 0),
      (time(6), 5),
      (time(8, 30), 12),
      (time(11, 59, 59), 4),
      (time(18), 10),
      (time(23, 30), -1),
    ])

    from datetime import datetime, timedelta
    date_chart = pygal.Line(x_label_rotation=20)
    date_chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'), [
     datetime(2013, 1, 2),
     datetime(2013, 1, 12),
     datetime(2013, 2, 2),
     datetime(2013, 2, 22)])
    date_chart.add("Посещаемость", [300, 412, 823, 672])


    return render(req,'blog/statistics.html',{'graph':bc.render_data_uri(),'line_chart':line_chart.render_data_uri(),'time':dateline.render_data_uri(),'date':date_chart.render_data_uri()})
