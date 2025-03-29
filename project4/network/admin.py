from django.contrib import admin

# Register your models here.

from .models import Post, User, Comment

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Comment)