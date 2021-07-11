from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORIES = (
        ('Fashion','Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'),
        ('Other', 'Other')
    )
DURATIONS = (
        (1, "24 Hours"),
        (7, "1 Week"),
        (14, "2 Weeks"),
        (21, "3 Weeks"),
        (30, "1 Month")
    )

class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Listing Details
    title = models.CharField(max_length=64) # listing title
    image = models.URLField(blank=True) # listing image
    description = models.CharField(max_length=512) # listing description
    category = models.CharField(max_length=64, choices=CATEGORIES) # listing category

    # Status
    created = models.DateTimeField() # date and time the listing was created
    end = models.DateTimeField() # date and time the listing ends
    duration = models.CharField(max_length=64, choices=DURATIONS) # how long the listing will be active
    active = models.BooleanField(default=True) # is listing active?

    # Bidding
    current_bid = models.DecimalField(max_digits=24, decimal_places=2)
    total_bids = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    def new_bid(self):
        """
        Updates the current_bid value when a new bid is made. 
        """
        pass



class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # what user made the bid
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE) # the listing user bidded on
    bid = models.DecimalField(max_digits=24, decimal_places=2) # bid amount 
    date = models.DateTimeField() # date bid was made

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # user that made comment
    #listing = models.ForeignKey(Listing, on_delete=models.CASCADE) # listing commented on
    content = models.CharField(max_length=256) # content of the actual comment
    date = models.DateTimeField() # date comment was made
    