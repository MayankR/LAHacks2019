from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from dotenv import load_dotenv
import os

# Create your views here.


def index(request):
    return HttpResponse("yo");

@csrf_exempt 
def msg(request):
    name = request.POST.get('Body', '')

    r = MessagingResponse()
    r.message("Killin' it at LAHacks! You sent: " + name)

    return HttpResponse(r.to_xml(), content_type='text/xml')

def test(request):
    load_dotenv()
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                         from_='+18582390484',
                         to='+18585317069'
                     )

    print(message.sid)

    return HttpResponse("yolo");