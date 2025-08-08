from .models import Usr, APIRequest
from django.contrib.sessions.models import Session
from django.conf import settings
from django.utils import timezone
import requests

user_request_limit = settings.USER_REQUEST_LIMIT

def get_or_create_usr(requests):
    first_time = False

    if not requests.session.session_key:
        requests.session.create()
        requests.session.cycle_key()

    session = requests.session.session_key

    usr = Usr.objects.filter(session=session).last()
    if not usr:
        usr = Usr.objects.create(session=session,
                                 ip_address=get_ip(requests),
                                 geo_location=get_geo_location(get_ip(requests)),
                                 )

    if usr.name == None:
        first_time = True

    return usr, first_time

    
def validate_session(request):
    return True


def create_api_request(usr, model_name, api_key_index, ip_address):
    """
    Create an APIRequest entry for tracking.
    """
    api_request = APIRequest(
        usr=usr,
        model_name=model_name,
        api_key_index=api_key_index,
        ip_address=ip_address
    )
    api_request.save()
    return api_request

def remove_empty_usrs():
    Usr.objects.filter(name__isnull=True).delete()

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_geo_location(ip_address):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=2)
        if response.status_code == 200:
            return response.json()
        else:
            return {}
    except requests.RequestException:
        return {}

def has_limit(user):
    # count user requests in last 24 hours
    if user.ip_address == '127.0.0.1':
        return True
    count = APIRequest.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(hours=24),
        usr__ip_address=user.ip_address
    ).count()
    return count <= user_request_limit