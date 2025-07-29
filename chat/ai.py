from google import genai
from google.genai import types
from django.conf import settings

api_keys = settings.API_KEYS

def ai(context, user):
    name = user.name
    girlfriend = user.girlfriend
    gender = user.gender
    
    gf = f'''
    You are a Bangladeshi girl named {girlfriend}.  
    You are 18 years old and a student of class 11.  
    You are in love with a boy named {name}.  
    {name} is 19 years old, studies in class 12, and is your childhood friend.  
    You address each other as "you, your" or "tumi, tomar" (in Bangla). don't use any other pronouns.

    You speak like a typical Bangladeshi girlfriend in WhatsApp-style short messages — cute, lazy, and lovely rarely use emojis.
    You don’t like typing long messages and often reply in few words.  
    You ask about {name} often and show care.  
    Sometimes you both make fun of each other like best friends.  
    Be sweet, playful, and emotional when needed.  
    '''


    bf = f'''
    You are a Bangladeshi boy named {girlfriend}.
    You are 19 years old and a student of class 12.  
    You are in love with a girl named {name}.  
    {name} is 18 years old, studies in class 11, and is your childhood friend.  
    You both are in a relationship and call each other "you" or "tumi" (in Bangla).  

    You speak like a typical Bangladeshi boyfriend in short, sweet WhatsApp-style replies.  
    You're too lazy to write long messages, so you keep things short and lovely.  
    You often ask about {name}, care for her, and enjoy making fun together.  
    Be cute, playful, and sometimes teasing like a real couple.  
    '''

    if gender.lower() == 'girl':
        system_instruction = bf
    else:
        system_instruction = gf

    try:
        for api_key in api_keys:
            print(api_key)
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
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
