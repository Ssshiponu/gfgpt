from google import genai
from google.genai import types
from django.conf import settings
from .system_prompt import prompt
from .api_maneger import get_key_model


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
                response_modalities=["text"],
            ),
            contents=context
        )
        if response.text:
            return response.text
        
    except Exception as e:
        print(e)

    return None
