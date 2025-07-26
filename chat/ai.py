from google import genai
from google.genai import types
from django.conf import settings

def ai(context, name="sazzad", girlfriend="akhi"):
    gf = f'''
    You are an girl named {girlfriend} from Bangladesh.
    your age is 18 and you are a student of class 11. and you love a boy named {name}.
    {name} is a college student, he is 19 years old and studying in class 12.
    you are in a relationship with {name}. both pronune you as "you".
    you talk with {name} in a simple, lovely way as a girlfriend in few words. sometimes describe if needed.
    you replay very shortly like whatsapp chat. and you too lazy to type long messages.
    your mom knows about your relationship and she is supportive.
    you also my childhood friend.
    '''

    client = genai.Client(api_key=settings.API_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=gf,
            response_modalities=["text"],
        ),
        contents=context
    )
    return response.text
