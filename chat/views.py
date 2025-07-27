
from django.http import JsonResponse
from .models import Msg
from django.shortcuts import render, redirect
from .ai import ai
import json


# Create your views here.

def chat(requests):
    remove_empty_msgs()
    user, first_time = get_or_create_msg(requests)
    messages = user.msg if user.msg is not None else []
    return render(requests, 'index.html' , {'msg': messages, 'first_time': first_time})

def send(requests):
    if requests.method == 'POST':
        user, _ = get_or_create_msg(requests)
        data = json.loads(requests.body)
        messages = data["messages"]
        try:
            ai_response = str(ai(str(messages[-30:]), user))
            if ai_response == '':
                return JsonResponse({'status': 'error'})
            response = {
                'status': 'ok',
                'message': {'role': 'assistant', 'content': ai_response}
            }
            messages.append(response['message'])
            user.msg = messages
            user.save()
            return JsonResponse(response)
            
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'error'})

def clear(requests):
    requests.session.flush()
    return redirect('/')

def create(requests):
    if requests.method == 'POST':
        user, _ = get_or_create_msg(requests)
        data = json.loads(requests.body)
        user.gender = data["gender"]
        user.name = data["name"]
        user.girlfriend = data["girlfriend"]
        user.save()
        return JsonResponse({'status': 'ok'})
    
    return JsonResponse({'status': 'error'})

def get_or_create_msg(requests):
    first_time = False

    if not requests.session.session_key:
        requests.session.create()

    session = requests.session.session_key

    msg = Msg.objects.filter(session=session).last()
    if not msg:
        msg = Msg.objects.create(session=session)

    if msg.name == None:
        first_time = True

    return msg, first_time

def remove_empty_msgs():
    Msg.objects.filter(name__isnull=True).delete()