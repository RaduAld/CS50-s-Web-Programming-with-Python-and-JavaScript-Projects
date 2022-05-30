from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.id} {self.username} email {self.email}"

class Category(models.Model):
    categ = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.categ}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    image_url = models.CharField(max_length=1000000, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    categories = models.ManyToManyField(Category, blank=False, related_name="categories")
    active = models.BooleanField()

    def __str__(self):
        return f"{self.id} {self.title} by {self.user}"

class Bid(models.Model):
    bid = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_creator")
    listing_name = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_listing")
    
    def __str__(self):
        return f"{self.id} {self.bid} from {self.user} to {self.listing_name}"

class Comment(models.Model):
    text = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_creator")
    listing_name = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_listing")

    def __str__(self):
        return f"{self.id} {self.text} from {self.user} to {self.listing_name}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_owner")
    watchlist = models.ManyToManyField(Listing, blank=True,  related_name="watchlist")
    
    def __str__(self):
        return f"{self.user} {self.watchlist}"
