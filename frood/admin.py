from django.contrib import admin
from frood.models import Meetup, UserProfile,Review #importing UserProfile

admin.site.register(Meetup)
admin.site.register(UserProfile)
admin.site.register(Review)