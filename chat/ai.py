from google import genai
from google.genai import types
from django.conf import settings
from .system_prompt import prompt
from .api_maneger import get_key_model
from .utils import create_api_request


def ai(context, user):
    """Generate AI response using Google Gemini API."""
    
    system_instruction = prompt(user)
    api_key, model = get_key_model()
    
    # Try primary API key
    response = get_response(api_key, model, system_instruction, context)
    if response:
        create_api_request(user, model, settings.API_KEYS.index(api_key), user.ip_address)
        return response
    
    # Try other API keys if primary fails
    for key in settings.API_KEYS:
        if key == api_key:
            continue
        response = get_response(key, model, system_instruction, context)
        if response:
            create_api_request(user, model, settings.API_KEYS.index(key), user.ip_address)
            return response
    
    return None


def get_response(api_key, model, system_instruction, context):
    """Get response from Gemini API."""
    print(settings.API_KEYS.index(api_key))

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_modalities=["text"],
                response_mime_type="text/plain",
            ),
            contents=context
        )
        return response.text if response.text else None
    except Exception as e:
        print(e)
        return None