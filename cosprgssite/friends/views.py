__author__ = "Jeremy Nelson"

import os

from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from cosprgssite.settings import PROJECT_HOME
from friends.forms import FriendForm, PostalAddressForm
from friends.models import Friend, CommitteeMembership, PhoneNumber
from friends.models import PostalAddress

def default(request):
    if request.user.is_authenticated():
        friends = Friend.objects.all().order_by('user__last_name')
    else:
        friends = Friend.objects.filter(
            is_public=True).order_by(
                'user__last_name')
    half_size = len(friends) / 2 
    return render(request,
                  'friends.html',
                  {'category': 'about',
                   'slice1': friends[0: half_size],
                   'slice2': friends[half_size:],
                   'section': 'friend'})

def friend(request,
           username):
    custom_template = os.path.join(PROJECT_HOME,
                                   'cosprgssite',
                                   'templates',
                                   '{0}.html'.format(username))
    if username.endswith("/"):
        username = username[:-1]
    user_query = User.objects.all().filter(username=username)
    if len(user_query) < 1:
        raise Http404
    friend = Friend.objects.all().get(user=user_query[0])
    forms = None
    if not request.user.is_authenticated():
        if not friend.is_public:
            raise Http404
    if request.user == friend.user or request.user.is_superuser:
        forms = {'friend': FriendForm(instance=friend),
                 'post_addr': PostalAddressForm(
                     instance=friend.postal_address),
                 'user': UserChangeForm(instance=friend.user)}
                 
        
    committees = CommitteeMembership.objects.all().filter(friend=friend)
    telephones = PhoneNumber.objects.filter(friends=friend)
    if not os.path.exists(custom_template):
        custom_template = 'friend.html'
    return render(request,
                  custom_template,
                  {'category': 'about',
                   'committees': committees,
                   'forms': forms,
                   'info': friend,
                   'section': 'friend',
                   'telephones': telephones,
                   'username': username})

def update(request):
    friend = Friend.objects.get(pk=request.POST.get('friend_id'))
    friend_form = FriendForm(request.POST,
                             instance=friend)
    postal_addr_form = PostalAddressForm(request.POST,
                                         instance=friend.postal_address)
    user_form = UserChangeForm(request.POST)
    if friend_form.is_valid() and \
       postal_addr_form.is_valid():
        postal_addr_form.save()
        friend_form.save()
        friend.user.first_name = request.POST.get('first_name')
        friend.user.last_name = request.POST.get('last_name')
        friend.user.email = request.POST.get('email')
        friend.user.save()
        return redirect("/Friends/{0}".format(friend.user.username))
    else:
        friend = friend
        forms = {'friend': friend_form ,
                 'post_addr': postal_addr_form ,
                 'user': user_form}
        return render(request,
                  custom_template,
                  {'category': 'about',
                   'committees': committees,
                   'forms': forms,
                   'info': friend,
                   'section': 'friend',
                   'username': username})        
    
