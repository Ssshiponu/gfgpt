
from django.http import JsonResponse
from django.utils.html import escape
from datetime import datetime
from .models import Usr, SEO
from django.shortcuts import render, redirect
from .ai import ai
from .profanity import check_profanity
import json
from .utils import *
from django.conf import settings

def robots(requests):
    return render(requests, 'robots.txt', content_type="text/plain",
                context={'sitemap_url': 'https://' + requests.get_host() + '/sitemap.xml'})

def sitemap(requests):
    return render(requests, 'sitemap.xml', content_type="application/xml",
                context={'url': 'https://' + requests.get_host(), 'lastmod': datetime.now().strftime('%Y-%m-%d')})


def chat(requests):
    user, first_time = get_or_create_usr(requests)
    
    messages = user.messages if user.messages is not None else []
    seo = SEO.objects.all().first()

    context = {
        'user': user,
        'messages': messages,
        'settings': user.settings,
        'first_time': first_time,
        'languages': Usr.languages,
        'use_emojis': Usr.use_emojis,
        'pronouns': Usr.pronouns,
        'personalities': Usr.personalities,
        'tones': Usr.tones,
        # SEO
        'name': seo.name if seo else '',
        'altname': seo.altname if seo else '',
        'title': seo.title if seo else '',
        'description': seo.description if seo else '',
        'keywords': seo.keywords if seo else '',
        'author': seo.author if seo else '',
        'url': requests.build_absolute_uri('/'),
        'share_text': 'Check out this cool app!',
    }

    return render(requests, 'index.html', context)


def send(requests):
    if not validate_session(requests):
        return JsonResponse({'status': 'error', 'message': 'Invalid session'})

    if requests.method == 'POST':
        user, _ = get_or_create_usr(requests)
        messages = user.messages if user.messages is not None else []
        data = json.loads(requests.body)
        message = escape(data["content"])
        ai_request = str(messages[-(settings.MAX_REMEMBERED_MESSAGES):] + [data])

        try: 
            # Check profanity
            is_bad, words = check_profanity(message)
            if is_bad:
                return JsonResponse({'status': 'rejected', 'words': words})
            
            if not has_limit(user):
                return JsonResponse({'status': 'error', 'message': 'Your daily message limit has been reached. Please try again tomorrow.'})

            raw_ai_response = ai(ai_request, user)

            # check if AI response is empty
            if raw_ai_response is None:
                return JsonResponse({'status': 'error', 'message': 'No Response.'})
            
            ai_response = str(raw_ai_response)
            
            response = {
                'status': 'ok',
                'message': {'role': 'assistant', 'content': ai_response}
            }
            messages.append(data)
            messages.append(response['message'])
            user.messages = messages
            user.save()
            print(f"{user.name}: {message}")
            print(f"AI: {ai_response}")
            return JsonResponse(response)
            
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': 'An error occurred while processing your request.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def clear(requests):
    if not validate_session(requests):
        return JsonResponse({'status': 'error', 'message': 'Invalid session'})

    requests.session.flush()
    return redirect('/')

def create(requests):
    if not validate_session(requests):
        return JsonResponse({'status': 'error', 'message': 'Invalid session'})

    if requests.method == 'POST':
        remove_empty_usrs()
        user, _ = get_or_create_usr(requests)
        data = json.loads(requests.body)

        validation_cases = [
            (data["gender"].lower() not in ["boy", "girl"], "Invalid gender."),
            (len(data["name"]) < 3, "Name is too short."),
            (len(data["girlfriend"]) < 3, "Girlfriend name is too short."),
            (len(data["name"]) > 20, "Name is too long."),
            (len(data["girlfriend"]) > 20, "Girlfriend name is too long.")
        ]

        for case, message in validation_cases:
            if case:
                return JsonResponse({'status': 'error', 'message': message})
            
        user.gender = data["gender"]
        user.name = data["name"]
        user.girlfriend = data["girlfriend"]
        user.settings = Usr.default_usr_settings()
        user.ip_address = get_ip(requests)
        user.geo_location = get_geo_location(user.ip_address)
        user.save()
        print(f'User created: {user.name}, {user.girlfriend}' )
        return JsonResponse({'status': 'ok'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def user_settings(request):
    if not validate_session(request):
        return JsonResponse({'status': 'error', 'message': 'Invalid session'})

    if request.method == 'POST':
        user, _ = get_or_create_usr(request)
        try:
            
            data = json.loads(request.body)
            form_action = data.get("formAction")

            if form_action == 'reset':
                user.settings = Usr.default_usr_settings()
                user.save()
                return JsonResponse({'status': 'ok', 'message': 'Settings updated successfully.'})

            language = data.get("language", "")
            use_emojis = data.get("use_emojis", "")
            pronoun = data.get("pronoun", "")
            personality = data.get("personality", "")
            tone = data.get("tone", "")

            # Validate the data
            validation_cases = [
                (language not in Usr.languages, 'Invalid language.'),
                (use_emojis not in Usr.use_emojis, 'Invalid emoji preference.'),
                (pronoun not in Usr.pronouns.get(language, []), 'Invalid pronoun.'),
                (personality not in Usr.personalities, 'Invalid personality.'),
                (tone not in Usr.tones, 'Invalid tone.')
            ]
            for case, message in validation_cases:
                if case:
                    return JsonResponse({'status': 'error', 'message': message})

            if form_action == 'update':
                user.settings = {
                    "language": language,
                    "use_emojis": use_emojis,
                    "pronoun": pronoun,
                    "personality": personality,
                    "tone": tone
                }
                user.save()
                return JsonResponse({'status': 'ok', 'message': 'Settings updated successfully.'})
                
            
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': 'Invalid data or server error.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})