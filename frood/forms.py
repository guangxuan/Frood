from django import forms
from frood.models import Meetup, User, UserProfile, Review
from django.contrib.admin import widgets

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('interests', 'picture')

class MeetupForm(forms.ModelForm):

    datetime = forms.DateTimeField(initial='YYYY-MM-DD HH:MM:SS')
    #location

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Meetup
        fields = ('name', 'copay','datetime')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'description')