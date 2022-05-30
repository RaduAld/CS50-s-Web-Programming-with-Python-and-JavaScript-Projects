from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("User", related_name="user_followers", blank=True)
    following = models.ManyToManyField("User", related_name="user_following", blank=True)

    def __str__(self):
        return f"{self.id}. {self.username}"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "followers": [user.username for user in self.followers.all()],
            "following": [user.username for user in self.following.all()]
        }


class Post(models.Model):
    creator = models.ForeignKey("User", on_delete=models.CASCADE, related_name="post_origin")
    body = models.TextField(max_length=500, blank=False)
    likes = models.ManyToManyField("User", related_name="like_user", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}. --{self.creator.username} ON {self.timestamp}"

    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator.username,
            "body": self.body,
            "likes": [user.username for user in self.likes.all()],
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }
