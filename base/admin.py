from django.contrib import admin

# Register your models here.

from .models import Post, Topic, Comment, User

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Topic)
admin.site.register(Comment)