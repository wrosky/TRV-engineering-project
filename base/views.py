from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Post, Topic, Comment
from .forms import PostForm

@login_required(login_url='login')
def profilePage(request):
    return render(request, 'base/profile.html')

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password is incorrect')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User was created successfully, login to continue')
            return redirect('login')
        else:
            messages.error(request, 'An error has occured during registration')

    context = {'form': form}
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Post.objects.filter(
        Q(topic__name__icontains=q) |
        Q(user_name__icontains=q) |
        Q(localisation__icontains=q)
        )

    topics = Topic.objects.all()
    post_count = posts.count()
    post_comments = Comment.objects.filter(Q(post__topic__name__icontains=q))

    context = {'posts': posts, 'topics': topics, 'post_count': post_count, 'post_comments': post_comments}
    return render(request, 'base/home.html', context)

def post(request, pk):
    post = Post.objects.get(id=pk)
    post_comments = post.comment_set.all().order_by('-date_created')
    participants = post.participants.all()

    if request.method == 'POST':
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            body=request.POST.get('body')
        )
        post.participants.add(request.user)
        return redirect('post', pk=post.id)

    context = {'post': post, 'post_comments': post_comments, 'participants': participants}
    return render(request, 'base/post.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    posts = user.post_set.all()
    post_comments = user.comment_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'posts': posts, 'post_comments': post_comments, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createPost(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.host = request.user
            post.rate = 1
            post.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/post_form.html', context)

@login_required(login_url='login')
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if request.user != post.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/post_form.html', context)

@login_required(login_url='login')
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    
    if request.user != post.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': post})

@login_required(login_url='login')
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    
    if request.user != comment.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        comment.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': comment})