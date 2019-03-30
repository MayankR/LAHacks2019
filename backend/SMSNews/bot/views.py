from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import UserInfo

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from dotenv import load_dotenv
import os

from . import utils

# Create your views here.


def index(request):
    return HttpResponse("yo");

@csrf_exempt 
def msg(request):
    print(request.POST)
    msg_body = request.POST.get('Body', '').lower()
    from_num = request.POST.get('From', '').lower()


    u = utils.get_current_user(from_num)

    if u.name == '*':
        resp = utils.get_new_user_text()
        u.name = '#'
        u.save()
    elif u.name == '#':
        u.name = msg_body
        u.save()
        resp = utils.get_country_prompt(u)
    elif u.country == '*':
        resp = "Awesome, lets get you started"
        u.country = "#"
        u.save()
    elif msg_body == utils.HELP_CMD:
        resp = utils.get_help_text()
    elif msg_body == utils.NEWS_TOPICS_CMD:
        resp = utils.get_topics_list()
    else:
        resp = 'Unknown command. Enter "' + utils.HELP_CMD + '" for more info.'

    r = MessagingResponse()
    r.message(resp)

    return HttpResponse(r.to_xml(), content_type='text/xml')