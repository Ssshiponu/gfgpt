from .models import Msg

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

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



