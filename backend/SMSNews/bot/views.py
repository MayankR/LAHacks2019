from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

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
    name = request.POST.get('Body', '').lower()

    if name == utils.HELP_CMD:
        resp = utils.get_help_text()
    elif name == utils.NEWS_TOPICS_CMD:
        resp = utils.get_topics_list()
    else:
        resp = 'Unknown command. Enter "' + utils.HELP_CMD + '" for more info.'

    r = MessagingResponse()
    r.message(resp)

    return HttpResponse(r.to_xml(), content_type='text/xml')