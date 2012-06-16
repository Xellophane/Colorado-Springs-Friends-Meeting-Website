"""
 :mod:`views` 
"""
__author__ = 'Jeremy Nelson'

import datetime
from calendar import HTMLCalendar
from django.contrib.auth import authenticate
from django.views.generic.simple import direct_to_template
from events.models import MeetingEvent
from donate.forms import PersonForm
from quakers.forms import EmailContactForm

class Events(object):

    def __init__(self,**kwargs):
        self.events = []
        if 'meeting' in kwargs:
            self.events.append(kwargs.get('meeting'))

    def day_url(self,year,month,day,has_event=False):
        return ''

    def month_url(self,year,month):
        return ''

    def events_by_day(self,year,month):
        return dict()
                               

def email(request):
    """
    Default view for email receipt
    """
    pass

def home(request):
    """
    Default view for Colorado Springs Monthly Meeting Website
    """
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
    event_query = MeetingEvent.objects.all()
    events = Events()
    today = datetime.datetime.today()
    current_calendar = HTMLCalendar().formatmonth(today.year,today.month)
    return direct_to_template(request,
                              'index.html',
                             {'current_calendar':current_calendar,
                              'email_form':EmailContactForm(),
                              'person_form':PersonForm(),
                              'section':'testimonies',
                              'user':user})
