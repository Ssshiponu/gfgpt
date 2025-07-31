from .models import APIRequest
from django.conf import settings
from django.utils import timezone

api_keys = settings.API_KEYS

# AI models limit
ai_models = {

    'gemini-2.5-flash': {
        'rpm': 10,
        'rpd': 250
    },
    'gemini-2.5-pro': {
        'rpm': 5,
        'rpd': 100
    },
    # 'gemini-2.5-flash-lite': {
    #     'rpm': 3,
    #     'rpd': 1000
    # },
}

# main function to get the API key and model name based on the limits
def get_key_model():

    for api_key_index, api_key in enumerate(api_keys):
       for name, limit in ai_models.items():
            rpm, rpd = get_counts(name, api_key_index)
            if rpm < limit['rpm'] and rpd < limit['rpd']:
                return api_key, name

    return None, None


def get_counts(model_name, api_key_index):
    now = timezone.now()
    
    # Get both counts in one query with aggregation
    from django.db.models import Count, Q
    
    counts = APIRequest.objects.filter(
        api_key_index=api_key_index, 
        model_name=model_name
    ).aggregate(
        rpm_count=Count('id', filter=Q(created_at__gte=now - timezone.timedelta(minutes=1))),
        rpd_count=Count('id', filter=Q(created_at__gte=now - timezone.timedelta(hours=24)))
    )

    print('counts:',counts)
    
    return counts['rpm_count'], counts['rpd_count']



