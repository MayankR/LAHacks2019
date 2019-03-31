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

    # if u.name == '*':
    #     resp = utils.get_new_user_text()
    #     u.name = '#'
    #     u.save()
    # elif u.name == '#':
    #     u.name = msg_body
    #     u.save()
    #     resp = utils.get_greeting(u) + " " + utils.get_country_prompt(u)
    # el
    if u.country == '*':
        resp = utils.get_new_user_text() + "\n" + utils.get_country_prompt()
        u.country = '#'
        u.save()
    elif msg_body in utils.COUNTRY_CMD:
        resp = utils.get_country_prompt()
        u.country = '#'
        u.save()
    elif u.country == '#':
        if not utils.check_if_num_in_range(msg_body):
            resp = 'Enter a valid number \n'
            resp += utils.get_country_prompt()
        else:
            u.country = int(msg_body)-1
            u.topic_idx = 0
            u.save()
            resp = "Awesome, lets get you started! \n"
            resp += utils.get_topics_list(u)
    elif msg_body in utils.HELP_CMD:
        resp = utils.get_help_text()
    elif msg_body in utils.NEWS_TOPICS_CMD:
        u.topic_idx = 0
        u.save()
        resp = utils.get_topics_list(u)
    elif msg_body == 'm':
        resp = utils.get_topics_list(u)
    elif utils.check_if_num_in_range(msg_body):
        utils.get_topic_news(u, int(msg_body)-1)
        resp = "Info here"
    else:
        resp = 'Unknown command. Enter "' + utils.HELP_CMD[0] + '" for help.'

    r = MessagingResponse()
    r.message(resp)

    return HttpResponse(r.to_xml(), content_type='text/xml')