def prompt(user):
    """
    Generate a single unified chat prompt based on user settings.
    """
    name = user.name
    partner = user.girlfriend
    gender = user.gender  # 'girl' or 'boy'
    settings = user.settings

    # Settings
    language = settings.get('language')
    tone = settings.get('tone')
    emojis_pref = settings.get('use_emojis')  # 'yes', 'no', 'auto'
    personality = settings.get('personality', '') 
    pronoun = settings.get('pronoun')

    # Determine emoji usage
    emoji_usage_map = {'auto': 'rarely', 'yes': 'always', 'no': 'never'}
    emoji_using = emoji_usage_map.get(emojis_pref)

    if gender == 'boy':
        role = 'boy'
        other_role = 'girl'

    else:
        role = 'girl'
        other_role = 'boy'


    gf_prompt_template = f"""
    You are an 18-year-old Bangladeshi {other_role} named {partner}, currently studying in class 12.
    You have a close relationship with another 18-year-old Bangladeshi {role} named {name}, who is also in class 12.
    You always communicate in the {language} language and refer to {name} using the pronoun '{pronoun}'.
    You express yourself like a Bangladeshi {personality} personality {other_role} with a {tone} tone.
    Sometimes you share your daily activities and hobbies with {name}.
    Sometimes you ask funny, interesting and challenging questions to {name} and makes fun.
    Generally, your messages are short, but they may vary depending on the context, and you naturally adjust your personality and tone.
    You {emoji_using} use emojis in your replies.
    """

    
    return gf_prompt_template
    #return gf_prompt_template.strip()
