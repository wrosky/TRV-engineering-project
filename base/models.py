from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.utils import timezone
from django_countries.fields import CountryField

class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, default='user-avatar.svg')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend_list')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends')

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        remover_friends_list = self
        remover_friends_list.remove_friend(removee)

        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False

class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        sender_friend_list, created = FriendList.objects.get_or_create(user=self.sender)
        receiver_friend_list, created = FriendList.objects.get_or_create(user=self.receiver)

        if sender_friend_list and receiver_friend_list:
            sender_friend_list.add_friend(self.receiver)
            receiver_friend_list.add_friend(self.sender)
            self.is_active = False
            self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()

class Post(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    rate = models.IntegerField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    likes = models.IntegerField(default=0)
    latitude = models.DecimalField(max_digits=20, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=16, blank=True, null=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.body[0:25]

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    def __str__(self):
        return self.user.username

class ChatGroup(models.Model):
    group_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.group_name

class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.author.username} : {self.body}'

class PrivateChat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_initiated')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_received')

    def __str__(self):
        return f"Chat between {self.user1.username} and {self.user2.username}"

class PrivateMessage(models.Model):
    chat = models.ForeignKey(PrivateChat, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.body}"

class Trip(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    country = CountryField()
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    num_days = models.PositiveIntegerField(default=0)

    flight_from = models.CharField(max_length=100, null=True, blank=True)
    flight_from_airport = models.CharField(max_length=100, null=True, blank=True)
    flight_to = models.CharField(max_length=100, null=True, blank=True)
    flight_to_airport = models.CharField(max_length=100, null=True, blank=True)

    flight_back_from = models.CharField(max_length=100, null=True, blank=True)
    flight_back_from_airport = models.CharField(max_length=100, null=True, blank=True)
    flight_back_to = models.CharField(max_length=100, null=True, blank=True)
    flight_back_to_airport = models.CharField(max_length=100, null=True, blank=True)

    flight_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    car_time = models.DurationField(null=True, blank=True)
    car_price_per_person = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    accommodation_name = models.CharField(max_length=100)
    accommodation_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    transport_type = models.CharField(max_length=100)
    transport_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    visa_required = models.BooleanField(default=False)
    visa_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

    total_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.flight_price = self.flight_price or 0
        self.car_price_per_person = self.car_price_per_person or 0
        self.accommodation_price = self.accommodation_price or 0
        self.transport_price = self.transport_price or 0
        self.visa_price = self.visa_price or 0

        self.total_price = (
            self.flight_price +
            self.car_price_per_person +
            self.accommodation_price +
            self.transport_price +
            self.visa_price
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title