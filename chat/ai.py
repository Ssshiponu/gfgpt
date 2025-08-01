from google import genai
from google.genai import types
from django.conf import settings
from .system_prompt import prompt
from .api_maneger import get_key_model
from .utils import create_api_request


def ai(context, user):
    """
    Generate AI response using Google Gemini API.
    """

    system_instruction = prompt(user)
    api_key, model = get_key_model()

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                #thinking_config=types.ThinkingConfig(thinking_budget=0),
                response_modalities=["text"],
                response_mime_type="text/plain",
            ),
            contents=context
        )
        if response.text is not None:
            create_api_request(
                usr=user,
                model_name=model,
                api_key_index=settings.API_KEYS.index(api_key),
                ip_address=user.ip_address
            )
            return response.text
        
    except Exception as e:
        print(e)

    return None
