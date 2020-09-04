from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass


class Listing(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=64,null=True)
    description = models.TextField(max_length=256,null=True)
    starting_bid = models.PositiveSmallIntegerField(null=True)
    price = models.PositiveSmallIntegerField(null=True)
    image_url = models.URLField(max_length=256,null=True)
    category = models.CharField(max_length=64,null=True)
    active = models.BooleanField(default=True)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,null=True)




class Bid(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,null=True)

class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,null=True)
    comments = models.CharField(max_length=256,null=True)
