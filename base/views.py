from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from amadeus import Client, ResponseError
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
from .models import *
from .forms import *

amadeus = Client(
    client_id=settings.AMADEUS_CLIENT_ID,
    client_secret=settings.AMADEUS_CLIENT_SECRET
)

@login_required(login_url='login')
def profilePage(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.post_set.all()
    post_comments = user.comment_set.all()

    is_own_profile = user == request.user

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
        'friend_requests': friend_requests,
        'is_friend': is_friend,
        'friends': friend_list if is_own_profile else None
    }
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def search_non_friends(request):
    query = request.GET.get('q', '')
    user = request.user
    friends = user.friend_list.friends.all()

    if query:
        non_friends = User.objects.filter(
            Q(username__icontains=query) | Q(name__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).exclude(id__in=friends.values_list('id', flat=True)).exclude(id=user.id)
    else:
        non_friends = User.objects.none()

    context = {'non_friends': non_friends, 'query': query}
    return render(request, 'base/search_non_friends.html', context)

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

@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    user = request.user
    friends = user.friend_list.friends.all()

    posts = Post.objects.filter(
        Q(host__in=friends) | Q(host=user)
    ).filter(
        Q(title__icontains=q) | Q(country__icontains=q) | Q(city__icontains=q)
    )

    post_count = posts.count()
    context = {'posts': posts, 'post_count': post_count}
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
        images = request.FILES.getlist('images')
        if form.is_valid():
            post = form.save(commit=False)
            post.host = request.user
            post.latitude = round(post.latitude, 8) if post.latitude else None
            post.longitude = round(post.longitude, 8) if post.longitude else None
            post.save()
            for image in images:
                PostImage.objects.create(post=post, image=image)
            return redirect('home')

    context = {'form': form, 'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY}
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
def download_trip_pdf(request, pk):
    trip = Trip.objects.get(pk=pk)

    font_path = os.path.join(settings.BASE_DIR, "static", "fonts", "Arial.ttf")
    pdfmetrics.registerFont(TTFont('Arial', font_path))
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="trip_{trip.title}.pdf"'
    
    p = canvas.Canvas(response, pagesize=A4)
    p.setFont("Arial", 12)

    p.drawString(100, 800, f"{trip.title}")
    p.drawString(100, 780, f"Country: {trip.country}")
    p.drawString(100, 760, f"Location: {trip.location}")
    p.drawString(100, 740, f"Start Date: {trip.start_date}")
    p.drawString(100, 720, f"End Date: {trip.end_date}")
    p.drawString(100, 700, f"Flight From: {trip.flight_from} " f"Airport: {trip.flight_from_airport}")
    p.drawString(100, 680, f"Flight To: {trip.flight_to} " f"Airport: {trip.flight_to_airport}")
    p.drawString(100, 660, f"Flight From: {trip.flight_back_from} " f"Airport: {trip.flight_back_from_airport}")
    p.drawString(100, 640, f"Flight To: {trip.flight_back_to} " f"Airport: {trip.flight_back_to_airport}")
    p.drawString(100, 620, f"Flight Price: {trip.flight_price} PLN")
    p.drawString(100, 600, f"Accommodation: {trip.accommodation_name}")
    p.drawString(100, 580, f"Accommodation Price: {trip.accommodation_price} PLN")
    
    p.drawString(100, 560, f"Total Price: {trip.total_price} PLN")
    
    p.showPage()
    p.save()
    
    return response

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
    
    user_has_liked = Likes.objects.filter(user=user, post=post).exists()
    
    if user_has_liked:
        Likes.objects.filter(user=user, post=post).delete()
        post.likes -= 1
    else:
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

@login_required(login_url='login')
def friend_chats(request):
    friend_list = request.user.friend_list.friends.all()
    return render(request, 'base/chat_components/friend_chats.html', {'friend_list': friend_list})

@login_required(login_url='login')
def chat(request):
    chat_group = get_object_or_404(ChatGroup, group_name='public-chat')
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message': message,
                'user': request.user
            }
            return render(request, 'base/chat_components/chat_message_p.html', context)

    return render(request, 'base/chat_components/chat.html', {'chat_messages': chat_messages, 'form': form})

@login_required(login_url='login')
def private_chat(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)

    chat = PrivateChat.objects.filter(
        user1=request.user, user2=friend
    ).first() or PrivateChat.objects.filter(
        user1=friend, user2=request.user
    ).first()
    
    if not chat:
        chat = PrivateChat.objects.create(user1=request.user, user2=friend)

    messages = chat.messages.all()
    form = PrivateMessageCreateForm()

    if request.method == 'POST' and request.htmx:
        form = PrivateMessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.author = request.user
            message.save()
            return render(request, 'base/chat_components/chat_message_p.html', {'message': message, 'user': request.user})

    return render(request, 'base/chat_components/private_chat.html', {'chat': chat, 'messages': messages, 'friend': friend, 'form': form})

@login_required(login_url='login')
def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.author = request.user
            trip.save()
            form.save_m2m()
            return redirect('trip_detail', pk=trip.pk)
    else:
        form = TripForm()
    return render(request, 'base/trip_planner/create_trip.html', {'form': form})

@login_required(login_url='login')
def update_trip(request, pk):
    trip = Trip.objects.get(pk=pk)
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.author = request.user
            trip.save()
            form.save_m2m()
            return redirect('trip_detail', pk=trip.pk)
    else:
        form = TripForm(instance=trip)
    return render(request, 'base/trip_planner/update_trip.html', {'form': form})

@login_required(login_url='login')
def deleteTrip(request, pk):
    trip = Trip.objects.get(id=pk)
    
    if request.user != trip.author:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        trip.delete()
        return redirect('list_trips')

    return render(request, 'base/delete.html', {'obj': trip})

@login_required(login_url='login')
def trip_detail(request, pk):
    trip = Trip.objects.get(pk=pk)
    return render(request, 'base/trip_planner/trip_detail.html', {'trip': trip})

@login_required(login_url='login')
def list_trips(request):
    trips = Trip.objects.filter(author=request.user)
    return render(request, 'base/trip_planner/list_trips.html', {'trips': trips})

@login_required(login_url='login')
def search_flight(request):
    if request.method == 'POST':
        origin = request.POST.get('from')
        destination = request.POST.get('to')
        departure_date = request.POST.get('departure_date')
        return_date = request.POST.get('return_date')
        
        try:
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=departure_date,
                returnDate=return_date,
                adults=1
            )
            flights = response.data
        except ResponseError as error:
            flights = []
            print(error)

        return render(request, 'base/flight_search/search_results.html', {'flights': flights})

    return render(request, 'base/flight_search/search_flight.html')

@login_required(login_url='login')
def airport_autocomplete(request):
    query = request.GET.get('term', '')
    if query:
        try:
            response = amadeus.reference_data.locations.get(
                keyword=query,
                subType='AIRPORT,CITY'
            )
            suggestions = [
                {
                    'label': f"{result['iataCode']} - {result['name']} ({result['address']['cityName']})",
                    'value': result['iataCode']
                }
                for result in response.data
            ]
        except ResponseError as error:
            suggestions = []
            print(f"API Error: {error}")
    else:
        suggestions = []

    return JsonResponse(suggestions, safe=False)