
from django.http import JsonResponse
from .models import Usr
from django.shortcuts import render, redirect
from .ai import ai
from .profanity import check_profanity
import json
from .utils import *
from django.conf import settings as st


def chat(requests):
    remove_empty_usrs()
    user, first_time = get_or_create_usr(requests)
    messages = user.messages if user.messages is not None else []

    context = {'user': user,
               'messages': messages,
               'settings': user.settings,
               'first_time': first_time,
               'languages': Usr.languages,
               'use_emojis': Usr.use_emojis,
               'pronouns': Usr.pronouns,
               'personalities': Usr.personalities,
               'tones': Usr.tones}

    return render(requests, 'index.html', context)


def send(requests):
    if requests.method == 'POST':
        user, _ = get_or_create_usr(requests)
        messages = user.messages if user.messages is not None else []
        data = json.loads(requests.body)
        message = data["content"]
        ai_request = str(messages[-(st.MAX_REMEMBERED_MESSAGES):] + [data])
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
            user.messages = messages
            user.save()
            print(f"User: {message}")
            print(f"AI: {ai_response}")
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
        user, _ = get_or_create_usr(requests)
        data = json.loads(requests.body)
        user.gender = data["gender"]
        user.name = data["name"]
        user.girlfriend = data["girlfriend"]
        user.settings = Usr.default_usr_settings()
        user.ip_address = get_ip(requests)
        user.geo_location = get_geo_location(user.ip_address)
        user.save()
        return JsonResponse({'status': 'ok'})
    
    return JsonResponse({'status': 'error'})


def settings(request):
    if request.method == 'POST':
        user, _ = get_or_create_usr(request)
        try:
            data = json.loads(request.body)
            form_action = data.get("formAction")
            language = data.get("language", "")
            use_emojis = data.get("use_emojis", "")
            pronoun = data.get("pronoun", "")
            personality = data.get("personality", "")
            tone = data.get("tone", "")

            # Validate the data
            if language not in Usr.languages:
                return JsonResponse({'status': 'error', 'message': 'Invalid language.'})
            if use_emojis not in Usr.use_emojis:
                return JsonResponse({'status': 'error', 'message': 'Invalid emoji preference.'})
            if pronoun not in Usr.pronouns[language]:
                print(pronoun, Usr.pronouns[language])
                return JsonResponse({'status': 'error', 'message': 'Invalid pronoun.'})
            if personality not in Usr.personalities:
                return JsonResponse({'status': 'error', 'message': 'Invalid personality.'})
            if tone not in Usr.tones:
                return JsonResponse({'status': 'error', 'message': 'Invalid tone.'})

            if form_action == 'update':
                user.settings = {
                    "language": language,
                    "use_emojis": use_emojis,
                    "pronoun": pronoun,
                    "personality": personality,
                    "tone": tone
                }
                
            elif form_action == 'reset':
                user.settings = Usr.default_usr_settings()
            user.save()
            return JsonResponse({'status': 'ok', 'message': 'Settings updated successfully.'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': 'Invalid data or server error.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})