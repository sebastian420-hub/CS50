from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

POST_CATEGORIES = [
    ('computer_graphics', '3D Computer Graphics'),
    ('graphic_designs', 'Graphic Designs'),
    ('threeD_models', '3D Models'),
    ('painting', 'Painting'),
    ('photography', 'Photography'),
    ('music', 'Music'),
]

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    post = models.TextField(max_length=200)
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="liked_posts")
    category = models.CharField(max_length=20, choices=POST_CATEGORIES, null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True) 
    timestamp = models.DateTimeField(auto_now_add=True)  

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "post": self.post,
            "image": self.image.url if self.image else '',
            "likes": self.likes.count(),
            "category": self.category if self.category else '',
            "link": self.link if self.link else '',
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

class Following(models.Model):
    following = models.ManyToManyField(User, related_name="followings")
    followers = models.ManyToManyField(User, related_name="followers")

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        
        return {
            "id": self.id,
            "user": self.user.username,
            "comments": self.comment,
            "timestamp": self.created
        }

