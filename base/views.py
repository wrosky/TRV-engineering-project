from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import Post, Topic, Comment, User, PostImage, FriendList, FriendRequest, Likes
from .forms import PostForm, EditUserForm

@login_required(login_url='login')
def profilePage(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.post_set.all()
    post_comments = user.comment_set.all()
    topics = Topic.objects.all()

    # Check if the user is viewing their own profile
    is_own_profile = user == request.user

    # Get the friend list of the user being viewed
    friend_list = None
    if is_own_profile:
        friend_list = request.user.friend_list.friends.all()

    is_friend = False
    if request.user.friend_list.friends.filter(id=user.id).exists():
        is_friend = True

    friend_requests = None
    if is_own_profile:
        friend_requests = FriendRequest.objects.filter(receiver=request.user, is_active=True)

    context = {
        'user': user,
        'posts': posts,
        'post_comments': post_comments,
        'topics': topics,
        'friend_requests': friend_requests,
        'is_friend': is_friend,
        'friends': friend_list if is_own_profile else None
    }
    return render(request, 'base/profile.html', context)

@login_required
def send_friend_request(request, user_id):
    sender = request.user
    receiver = get_object_or_404(User, id=user_id)
    
    if sender != receiver:
        friend_request, created = FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
        if created:
            messages.success(request, f'Friend request sent to {receiver.username}')
        else:
            messages.info(request, 'Friend request already sent')
    else:
        messages.warning(request, "You can't send a friend request to yourself")
    
    return redirect('user_profile', username=receiver.username)

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.receiver == request.user:
        friend_request.accept()
        messages.success(request, f'You are now friends with {friend_request.sender.username}')
    else:
        messages.error(request, 'You are not authorized to accept this friend request')
    
    return redirect('user_profile', username=friend_request.sender.username)

@login_required
def decline_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.receiver == request.user:
        friend_request.decline()
        messages.info(request, 'Friend request declined')
    else:
        messages.error(request, 'You are not authorized to decline this friend request')
    
    return redirect('user_profile', username=friend_request.sender.username)

@login_required
def cancel_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.sender == request.user:
        friend_request.cancel()
        messages.info(request, 'Friend request cancelled')
    else:
        messages.error(request, 'You are not authorized to cancel this friend request')
    
    return redirect('user_profile', username=friend_request.receiver.username)

@login_required
def remove_friend(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    friend_list = FriendList.objects.get(user=request.user)
    
    if friend_list.is_mutual_friend(friend):
        friend_list.unfriend(friend)
        messages.success(request, f'{friend.username} has been removed from your friends')
    else:
        messages.error(request, f'{friend.username} is not in your friend list')
    
    return redirect('user_profile', username=friend.username)

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email OR password is incorrect')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        elif password != password_confirm:
            messages.error(request, 'Passwords do not match')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
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
    user_has_liked = Likes.objects.filter(user=request.user, post=post).exists()

    if request.method == 'POST':
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            body=request.POST.get('body')
        )
        post.participants.add(request.user)
        return redirect('post', pk=post.id)

    context = {'post': post, 'post_comments': post_comments, 'participants': participants, 'user_has_liked': user_has_liked}
    return render(request, 'base/post.html', context)

@login_required(login_url='login')
def createPost(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        images = request.FILES.getlist('images')  # Collect multiple files here
        if form.is_valid():
            post = form.save(commit=False)
            post.host = request.user
            post.rate = 1
            post.save()
            for image in images:
                PostImage.objects.create(post=post, image=image)
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
def like(request, pk):
    user = request.user
    post = get_object_or_404(Post, id=pk)
    
    # Check if the user has already liked the post
    user_has_liked = Likes.objects.filter(user=user, post=post).exists()
    
    if user_has_liked:
        # If already liked, remove the like
        Likes.objects.filter(user=user, post=post).delete()
        post.likes -= 1
    else:
        # If not liked yet, add the like
        Likes.objects.create(user=user, post=post)
        post.likes += 1

    post.save()
    return HttpResponseRedirect(reverse('post', args=[str(pk)]))

@login_required(login_url='login')
def editUser(request):
    user = request.user
    form = EditUserForm(instance=user)

    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', username=user.username)

    context = {'form': form}
    return render(request, 'base/edit_user.html', context)