from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from frood.models import Meetup, UserProfile, Review
from frood.forms import MeetupForm,ReviewForm
from frood.forms import UserForm, UserProfileForm
from django.contrib.auth.models import User

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required    

from django.utils import simplejson

import hashlib

def decode_url(url):
    return url.replace(' ', '_')
  
def index(request):
    context = RequestContext(request)

    # Query for categories - add the list to our context dictionary.
    meetup_list = Meetup.objects.all()
    loclist=[]
    for meet in meetup_list:
        loclist.append([meet.name,meet.xcor,meet.ycor])
    jsonloc=simplejson.dumps(loclist);
    context_dict = {'meetups': meetup_list,'loc':jsonloc}

    # The following two lines are new.
    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
    # Render the response and return to the client.
    return render_to_response('frood/index.html', context_dict, context)

    
@login_required 
def meetup(request,meetup_name_url):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'meetup_name_url': meetup_name_url}
    context_dict['meetup_exists'] = False
    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        meetup = Meetup.objects.get(uid=meetup_name_url)
        loclist=[]
        loclist.append([meetup.name,meetup.xcor,meetup.ycor])
        jsonloc=simplejson.dumps(loclist);
        context_dict['loc']=jsonloc
        context_dict['meetup'] = meetup
        context_dict['iusers'] = meetup.iuser.all()
        context_dict['ishost'] = request.user.username == meetup.user.username
        context_dict['isjoin'] = request.user in meetup.iuser.all()
        context_dict['meetup_exists'] = True
    except Meetup.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render_to_response('frood/meetup.html', context_dict, context)

@login_required
def meetup_join(request,meetup_name_url):
    context = RequestContext(request)
    #context_dict = {'meetup_name_url': meetup_name_url}
    try:
        meetup = Meetup.objects.get(uid=meetup_name_url)
        if request.user not  in meetup.iuser.all():
            meetup.iuser.add(request.user)
    except Meetup.DoesNotExist:
        pass

    # Redirect
    return HttpResponseRedirect("/frood/meetup/"+meetup.uid+"/#content_block")

@login_required
def meetup_quit(request,meetup_name_url):
    context = RequestContext(request)
    #context_dict = {'meetup_name_url': meetup_name_url}
    try:
        meetup = Meetup.objects.get(uid=meetup_name_url)
        if request.user in meetup.iuser.all():
            meetup.iuser.remove(request.user)
    except Meetup.DoesNotExist:
        pass

    # Redirect
    return HttpResponseRedirect("/frood/meetup/"+meetup.uid+"/#content_block")

@login_required
def meetup_delete(request,meetup_name_url):
    context = RequestContext(request)
    #context_dict = {'meetup_name_url': meetup_name_url}
    try:
        meetup = Meetup.objects.get(uid=meetup_name_url)
        if request.user==meetup.user:
            meetup.delete()
    except Meetup.DoesNotExist:
        pass

    # Redirect
    return HttpResponseRedirect("/frood/")

@login_required
def select_location(request):
    context = RequestContext(request)

    # The following two lines are new.
    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
    # Render the response and return to the client.
    return render_to_response('frood/select_location.html', {}, context)


@login_required
def add_meetup(request,xcor,ycor):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = MeetupForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            new_meetup = form.save(commit=False) #don't commit first
            user = request.user
            
            hashlink = hashlib.md5()
            hashlink.update(str(user.username).encode('utf-8'))
            hashlink.update(str(Meetup.objects.all().count()).encode('utf-8'))
            
            new_meetup.uid = hashlink.hexdigest()
            new_meetup.xcor=xcor;
            new_meetup.ycor=ycor;
            new_meetup.user=user;
            new_meetup.save() #then save the form

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = MeetupForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('frood/add_meetup.html', {'form': form,'xcor':xcor,'ycor':ycor}, context)
  
def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'frood/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)


from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse  
def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            if user.is_active:  # Is the account active? It could have been disabled.
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/frood/')
            else:
                # An inactive account was used - no logging in!
                text = "Your Bookmark account is disabled."
                return render_to_response('frood/failedlogin.html', {'text':text}, context)
        else:
            # Bad login details were provided. So we can't log the user in.
            text = "Invalid login details supplied."
            print "Invalid login details: {0}, {1}".format(username, password)
            return render_to_response('frood/failedlogin.html', {'text':text}, context)
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('frood/login.html', {}, context)




@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/frood/')      
      
  
@login_required
def restricted(request):
    text = "Since you're logged in, you can see this text!"
    return render_to_response('frood/restricted.html', {'text':text}, RequestContext(request))

@login_required
def user_profile(request, username):
    context = RequestContext(request)
    try:
        c_user = User.objects.get(username = username)
        c_userprofile = UserProfile.objects.get(user=c_user)
        userimg = c_userprofile.picture
        userinterests = c_userprofile.interests
        reviews = Review.objects.filter(tuser=c_user)
        context_dict = {'username':c_user, 'userimg':userimg, 'userinterests':userinterests, 'reviews':reviews}
        return render_to_response('frood/user_profile.html', context_dict, RequestContext(request))
      
    except User.DoesNotExist:
        return render_to_response('frood/user_doesnotexist.html', {}, RequestContext(request))

@login_required    
def add_review(request,tusername):
    # Get the context from the request.
    context = RequestContext(request)
    distinct=True
    
    try:
        tuser = User.objects.get(username=tusername)
    except User.DoesNotExist:
        return render_to_response('frood/user_doesnotexist.html', {}, RequestContext(request))
    
    # A HTTP POST?
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            new_review = form.save(commit=False) #don't commit first
            fuser = request.user
            
            new_review.fuser=fuser;
            new_review.tuser=tuser;
            new_review.save() #then save the form

            # Now call the index() view.
            # The user will be shown the homepage.
            return user_profile(request,tusername)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        if(tuser!=request.user):
            form = ReviewForm()
            distinct=True
        else:
            form = ReviewForm()
            distinct=False
        
    return render_to_response('frood/add_review.html', {'form': form,'tuser':tuser,"distinct":distinct}, context)
    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    