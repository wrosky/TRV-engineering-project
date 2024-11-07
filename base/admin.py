from django.contrib import admin

# Register your models here.

from .models import *

class FriendListAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_filter = ['user']
    list_display = ['user']
    readonly_fields = ['user']

    class Meta:
        model = FriendList

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(FriendList, FriendListAdmin)
admin.site.register(ChatGroup)
admin.site.register(GroupMessage)
admin.site.register(PrivateChat)
admin.site.register(PrivateMessage)

class FriendRequestAdmin(admin.ModelAdmin):
    search_fields = ['sender__email', 'receiver__email', 'sender__username', 'receiver__username']
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver']

    class Meta:
        model = FriendRequest

admin.site.register(FriendRequest, FriendRequestAdmin)