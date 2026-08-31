from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.
class Movie(models.Model):
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=200)
    review=models.FloatField()
    active=models.BooleanField(default=True)


    def __str__(self):
        return self.name
class StreamPlatform(models.Model):
    name=models.CharField(max_length=10)
    about=models.CharField(max_length=20)
    website=models.URLField(max_length=50)
    def __str__(self):
        return self.name
class WatchList(models.Model):
    title=models.CharField(max_length=10)
    storyline=models.CharField(max_length=200)
    platform=models.ForeignKey(StreamPlatform,on_delete=models.CASCADE,related_name="watchlist"
   )
    average_rating=models.FloatField(default=0)
    number_rating=models.IntegerField(default=0)
    active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Review(models.Model):
    review_user=models.ForeignKey(User,on_delete=models.CASCADE)
    ratings=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description=models.CharField(max_length=200,null=True)
    watchlist=models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name="reviews")
    active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.ratings)+" "+self.watchlist.title
    

