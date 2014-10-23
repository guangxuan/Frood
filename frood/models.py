from django.db import models
from django.contrib.auth.models import User
from datetime import datetime    

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    interests = models.CharField(max_length = 25)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

# Create your models here.
class Meetup(models.Model):
    xcor = models.FloatField()
    ycor = models.FloatField()
    uid = models.CharField(max_length = 128)
    name = models.CharField(max_length = 25)
    COPAY_CHOICES= (
        ('TEN', '10%'),
        ('TWENTY', '20%'),
        ('THIRTY', '30%'),
        ('FORTY', '40%'),
        ('FIFTY', '50%'),
        ('SIXTY', '60%'),
        ('SEVENTY', '70%'),
        ('EIGHTY', '80%'),
        ('NINETY', '90%'),
        ('HUNDRED', '100%'),
    )
    user = models.ForeignKey(User,related_name="user")
    iuser = models.ManyToManyField(User,related_name="iuser")
    copay = models.CharField(choices = COPAY_CHOICES, max_length = 25)
    datetime = models.DateTimeField()
    #location
    def __unicode__(self):
        return (self.user, self.datetime)

class Review(models.Model):
    fuser = models.ForeignKey(User,related_name="fuser")
    tuser = models.ForeignKey(User,related_name="tuser")
    title = models.CharField(max_length = 25)
    description = models.CharField(max_length = 50)
    def __unicode__(self):
        return (self.title)