from django.shortcuts import render
from twilio.twiml.messaging_response import MessagingResponse
from .models import Customer, Content
# Create your views here.


def index():
    return ""


# at this time i am just coding the methods I will need.  I will integrate it in a bit
def send_message():
    response = MessagingResponse()
    contents = Content.get_content()
    texts = ""
    for content in contents:
        value = content.value*(10**(-1/content.value))
        update = Content.filter(id=content.id).update(value=value)
        update.save()
        texts += str(content.content) + "\n"
    response.message(texts)

    return str(response)


def receive_message(request):
    msg = request.form.get('Body').lower()
    user = request.form.get('From').lower()
    response = MessagingResponse()
    text = Content.get_content()
    resp = ""
    current_subject = ""
    if msg == "join egg-unusual" or msg == "hi":
        return send_message(user)
    else:
        user = Customer.objects.filter(phone=user).first()
        if user:
            new_content = Content(name=user, user_id=user.id, content=msg)
            new_content.save()
        else:
            new_user = Customer(name=user, phone=user)
            new_user.save()
            new_content = Content(name=new_user.name,
                                  user_id=new_user.id, content=msg)
            new_content.save()
        return send_message(user)

    return str(response)
