
from django.http import JsonResponse
from .models import Msg
from django.shortcuts import render, redirect
from .ai import ai
from .profanity import check_profanity
import json
import requests
from .utils import *

languages = {
    'bangla': 'বাংলা',
    'banglish': 'Banglish',
    'english': 'English',
    'hindi': 'हिंदी',
    'hindlish': 'Hinglish',
}

use_emojis = {
    'auto': 'Auto',
    'yes': 'Yes',
    'no': 'No',
}

pronouns = {
    'bangla': ['তুমি, তোমার', 'তুই, তোর', 'আপনি, আপনার'],
    'banglish': ['tumi, tomar', 'tui, tor', 'apni, apnar'],
    'english': ['you, your'],
    'hindi': ['तुम, तुम्हारा', 'तू, तेरा', 'आप, आपके'],
    'hindlish': ['tum, tumhara', 'tu, tera', 'aap, aapke'],
}

def chat(requests):
    remove_empty_msgs()
    user, first_time = get_or_create_msg(requests)
    messages = user.msg if user.msg is not None else []
    context = {'user': user, 'messages': messages, 'first_time': first_time,
               'languages': languages, 'use_emojis': use_emojis, 'pronouns': pronouns}
    
    return render(requests, 'index.html', context)


def send(requests):
    if requests.method == 'POST':
        user, _ = get_or_create_msg(requests)
        messages = user.msg if user.msg is not None else []
        data = json.loads(requests.body)
        ai_request = str(messages[-30:] + [data])
        message = data["content"]
        try: 
            # Check profanity
            is_bad, words = check_profanity(message)
            if is_bad:
                return JsonResponse({'status': 'rejected', 'words': words})

            ai_response = str(ai(ai_request, user))

            # check if AI response is empty
            if ai_response == '' or ai_response is None:
                return JsonResponse({'status': 'error', 'message': 'AI response is empty.'})
            
            response = {
                'status': 'ok',
                'message': {'role': 'assistant', 'content': ai_response}
            }
            messages.append(data)
            messages.append(response['message'])
            user.msg = messages
            user.save()
            return JsonResponse(response)
            
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': 'An error occurred while processing your request.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

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
        user.settings = {
            "language": 'bangla',
            "useEmojis": 'auto',
            "pronoun": 'tumi',
            "personality": 'friendly',
            "theme": 'romantic',
        }
        user.ip_address = get_ip(requests)
        user.save()
        return JsonResponse({'status': 'ok'})
    
    return JsonResponse({'status': 'error'})


    