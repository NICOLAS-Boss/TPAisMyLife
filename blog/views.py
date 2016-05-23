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


#def about(req):
#    return render(req,'blog/about.html',{})

def contacts(req):
    return render(req,'blog/contacts.html',{})




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
    bc = pygal.Bar()
    bc.add('посещаимость',[12,1,2,3,5,8,12,32,55])
    return render(req,'blog/statistics.html',{'graph':bc.render()})
