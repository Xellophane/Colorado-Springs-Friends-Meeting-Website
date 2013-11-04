__author__ = "Jeremy Nelson"

import os

from collections import OrderedDict
import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, authenticate
from friends.models import Committee, CommitteeMembership
from meetings import get_minute, get_minutes, QUAKER_MONTHS

def committee(request,
              committee):
    committee_ = Committee.objects.all().get(name=committee)
    committee_membership = CommitteeMembership.objects.all().filter(
        committee=committee_)
    return render(request,
                  '{0}.html'.format(committee.lower()),
                  {'category': 'about',
                   'section': 'committee',
                   'membership': committee_membership,
                   'reports': []})

def history(request,
            topic):
    return render(request,
                  '{0}.html'.format(topic),
                  {'category': 'about',
                   'section': 'history'})
                   

def home(request):
    return render(request,
                  'index.html',
                  {'category': 'home'})

def login_view(request):
    user = authenticate(username=request.POST.get('username'),
                        password=request.POST.get('secret'))
    if user is None:
        messages.error(request, "Username and/or Password invalid")
    return redirect("/")


def logout_view(request):
    logout(request)
    return redirect("/")

def meeting(request,
            meeting=None):
    if meeting:
        if meeting == 'Business':
            minutes = OrderedDict()
            all_minutes = get_minutes()
            for i,row in enumerate(all_minutes):
                if i > 0 or i <= len(all_minutes):
                    current_year = row.get('date').year
                    if current_year == all_minutes[i-1].get('date').year:
                        minutes[current_year].append(row)
                    else:
                        minutes[current_year] = [row,]
            return render(request,
                          'business.html',
                          {'category': 'about',
                           'minutes': minutes,
                           'section': 'meeting'})
                          
        return render(request,
                      '{0}.html'.format(meeting.lower()),
                      {'category': 'about',
                       'section': 'meeting'})
    else:
        return render(request,
                      'meetings.html',
                      {'category': 'about',
                       'section': 'meeting'})

def minute(request,
           meeting=None,
           year=None,
           month=None):
    if meeting:
        if meeting == 'Business':
            minute_html = get_minute(year,
                                     month)
            return render(request,
                          'minute.html',
                          {'category': 'about',
                           'content': minute_html,
                           'section': 'meeting'})
        
def report(request,
           committee,
           year,
           month):
    return HttpResponse("In report {0} {1} for {2}".format(
        committee,
        year,
        month))

def testimony(request,
              testimony=None):
    if testimony:
        return render(request,
                      '{0}.html'.format(testimony.lower()),
                      {'category':'about',
                       'section': 'testimonies'})
    else:
        return render(request,
                      'testimonies.html',
                      {'category':'about',
                       'section': 'testimonies'})
    
