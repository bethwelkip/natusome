from django.shortcuts import render
from twilio import twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from django_twilio.decorators import twilio_view
from .models import Customer, Content
from django.views.decorators.csrf import csrf_exempt
from decouple import config, Csv
import pandas as pd
import schedule
import time

# This initializes the database
def initialize_db():
        data = pd.read_csv('./natusome/sources/csv file name') # put file in 'sources' folder
        data.drop(['id','known'], axis=1,inplace = True)
        user = Customer.objects.filter(phone=config('MY_PHONE')).first()

        for row in data.itertuples():
            cont = "" + row[2] + "\n"+row[3]
            if row[1] == 2:
                new_content = Content(customer=user, content=cont, value = 111)
                new_content.save()
            else:
                new_content = Content(customer=user, content=cont)
                new_content.save()

# For the Home page
def index(request):
    # uncomment the line below to initialize thhe database
    # initialize_db() 
    return render(request, 'index.html')

# Method sends actual messages. Could modify to send to as many people as needed.
def _send_message():
    resp = Client(config('TWILIO_ACCOUNT_SID'), config('TWILIO_AUTH_TOKEN')) # get credentials from env
    contents = Content.get_content()
    texts = ""

    for content in contents:
        value = content.value*(10**(-1/content.value))
        update = Content.objects.filter(id=content.id).first()
        update.value = value
        update.save()
        texts += str(content.content) + "\n\n\n"

    message = resp.messages.create(to=config('MY_PHONE'), # MY_PHONE -> My personal phone number
    from_=config('TWILIO_ASSIGNED_NO'), #The sandbox twilio number
    body=texts)
    message.sid# send message

# At this time i am just coding the methods I will need.  I will integrate them in a bit.
def send_message(request):
    _send_message()
    return render(request, 'index.html')

# Send messages every 11.75 hours(Keep sandbox alive)
def schedule_message():
    _send_message()
    schedule.every(710).minutes.do(_send_message)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Register a new user
def register_new_user(user):
    new_user = Customer(name=user, phone=user)
    new_user.save()
    new_content = Content(customer=new_user.id, content=msg)
    new_content.save()

# Add user content
def add_content(user,cont):
    new_content = Content(customer=user, content=cont)
    new_content.save()


# Receive data for the db, activate sandbox, register new users if need be.
@csrf_exempt
@twilio_view
def receive_message(request):
    schedule_message()
    if request.method == 'POST':
        msg = request.POST.get('Body').lower()
        user = request.POST.get('From').lower()
        response = MessagingResponse()
        text = Content.get_content()
        resp = ""
        current_subject = ""
        print(user)
        if msg == "join egg-unusual" or msg == "hi" or msg == "join discover-feathers" :
            resp = "Thank you. \n To add content to your page reply to this with 'Commit + what you'd like to add.\n \n Otherwise reply with anything to receive new content"
            response.message(resp)
            return response

        elif msg.__contains__('commit'):
            msg = msg.replace("commit", '')
            user = Customer.objects.filter(phone=user).first()

            if user:        # if user exists, add their content and reschedule new content.
                add_content(user,msg)
                schedule_message()

            else:
                register_new_user(user)
                resp = f"Welcome! and Thank you.We have registered you as a new user with phone number{user[8:]}"
                response.message(resp, method='POST')
                return response
        else:
            schedule_message()

    return render(request, 'index.html')

    def parse_content_xlsx(request, file):
        # if user submits content via website and in excel format, parse it and store it.
        # Can use pandas if need be.
        # Ideally just two columns. The keyword and definition or the question and answer or question and hint.
        pass

    def parse_content_anki(request, file):
        # Same as above but for csv files
        pass
