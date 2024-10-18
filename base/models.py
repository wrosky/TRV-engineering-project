from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
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

class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    localisation = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    rate = models.IntegerField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

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