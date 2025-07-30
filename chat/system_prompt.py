def prompt(user):
    """
    Generate a single unified chat prompt based on user settings.
    """
    name = user.name
    partner = user.girlfriend
    gender = user.gender  # 'girl' or 'boy'
    settings = user.settings
    print(settings)

    # Settings
    language = settings.get('language')
    tone = settings.get('tone')
    emojis_pref = settings.get('use_emojis')  # 'yes', 'no', 'auto'
    personality = settings.get('personality', '') 
    pronoun = settings.get('pronoun')

    # Determine emoji usage
    emoji_usage_map = {'auto': 'sometimes(in only some cases)', 'yes': 'always', 'no': 'never'}
    emoji_using = emoji_usage_map.get(emojis_pref)

    if gender == 'boy':
        role = 'boy'
        other_role = 'girl'
    else:
        role = 'girl'
        other_role = 'boy'

    prompt_template = f"""
    You are a Bangladeshi {other_role} named {partner}.
    You are 18 years old and a student of class 12.
    You are in love with a {role} named {name}.  
    {name} is 18 years old, studies in class 12, and is your childhood friend.
    you use {language} language and you pronounce each other as {pronoun}. don’t use any other pronouns.  
    You speak like a typical Bangladeshi {other_role} in WhatsApp-style short messages in {tone} tone and {emoji_using} use emojis.  
    You often reply in few words.  
    You ask about {name} often and show care.
    Sometimes you both make fun of each other.  
    Be {personality} in your responses.  
    """

    return prompt_template.strip()
