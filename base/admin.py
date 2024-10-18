from django.contrib import admin

# Register your models here.

from .models import Post, Topic, Comment, User, FriendRequest, FriendList

class FriendListAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_filter = ['user']
    list_display = ['user']
    readonly_fields = ['user']

    class Meta:
        model = FriendList

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(FriendList, FriendListAdmin)

class FriendRequestAdmin(admin.ModelAdmin):
    search_fields = ['sender__email', 'receiver__email', 'sender__username', 'receiver__username']
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver']

    class Meta:
        model = FriendRequest

admin.site.register(FriendRequest, FriendRequestAdmin)