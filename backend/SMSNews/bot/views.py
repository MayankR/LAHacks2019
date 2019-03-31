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

    # load_dotenv()
    # account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    # auth_token = os.getenv("AUTH_TOKEN")

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
            u.do_hindi = -1
            u.save()
            if u.country == 2:
                resp = "Would you like all the news to be translated to Hindi?"
            else:
                resp = "Awesome, lets get you started! \n"
                resp += utils.get_topics_list(u)
    elif u.country == '2' and u.do_hindi == -1:
        if msg_body == "yes" or msg_body == 'y':
            u.do_hindi = 1
        else:
            u.do_hindi = 0
        u.save()
        resp = "Awesome, lets get you started! \n"
        resp += utils.get_topics_list(u)
    elif msg_body in utils.HELP_CMD:
        resp = utils.get_help_text()
    elif msg_body in utils.NEWS_TOPICS_CMD:
        u.topic_idx = 0
        u.url_idx = 0
        u.save()
        resp = utils.get_topics_list(u)
    elif msg_body == 'm' and u.url_idx == 0:
        resp = utils.get_topics_list(u)
        # else:
        # u.url_idx = 0
        # u.save()
    elif msg_body == 'm' and u.url_idx > 0:
        summ = utils.get_topic_news(u)
        print(summ)
        if summ == None:
            resp = "Unable to generate summary"
        else:
            resp = [summ]
            resp.append('Enter "N" to return to topics or "M" for news from more sources')
    elif utils.check_if_num_in_range(msg_body):
        u.topic_selected = int(msg_body)-1
        u.url_idx = 0
        u.save()
        summ = utils.get_topic_news(u)
        print(summ)
        if summ == None:
            resp = "Unable to generate summary"
        else:
            resp = [summ]
            resp.append('Enter "N" to return to topics or "M" for news from more sources')
    else:
        resp = 'Unknown command. Enter "' + utils.HELP_CMD[0] + '" for help.'

    r = MessagingResponse()
    if isinstance(resp, str):
        r.message(resp)
    else:
        for res in resp:
            r.message(res)

    # client = Client(account_sid, auth_token)

    # message = client.messages \
    #             .create(
    #                  body=resp,
    #                  from_=request.POST.get('To', ''),
    #                  to=request.POST.get('From', '')
    #              )

    # return HttpResponse("a")
    return HttpResponse(r.to_xml(), content_type='text/xml')