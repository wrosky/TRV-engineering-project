from django.shortcuts import render, redirect, get_object_or_404
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
def profilePage(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.post_set.all()
    post_comments = user.comment_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'posts': posts, 'post_comments': post_comments, 'topics': topics}
    return render(request, 'base/profile.html', context)

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
    page = 'register'

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif password != password_confirm:
            messages.error(request, 'Passwords do not match')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, 'Account created successfully')

            return redirect('login')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Post.objects.filter(
        Q(topic__name__icontains=q) |
        Q(title__icontains=q) |
        Q(localisation__icontains=q)
        )

    topics = Topic.objects.all()
    post_count = posts.count()
    post_comments = Comment.objects.filter(Q(post__topic__name__icontains=q))

    context = {'posts': posts, 'topics': topics, 'post_count': post_count, 'post_comments': post_comments}
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def createPost(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
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

@login_required(login_url='login')
def editUser(request):
    user = request.user
    form = UserCreationForm(instance=user)

    if request.method == 'POST':
        form = UserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/edit_user.html', context)