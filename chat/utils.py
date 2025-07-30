from .models import Usr
import requests

def get_or_create_usr(requests):
    first_time = False

    if not requests.session.session_key:
        requests.session.create()

    session = requests.session.session_key

    usr = Usr.objects.filter(session=session).last()
    if not usr:
        usr = Usr.objects.create(session=session)

    if usr.name == None:
        first_time = True

    return usr, first_time

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
        response = requests.get(f'http://ip-api.com/json/{ip_address}')
        if response.status_code == 200:
            return response.json()
        else:
            return {}
    except requests.RequestException:
        return {}

