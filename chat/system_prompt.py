def prompt(user):
    """
    Generate a single unified chat prompt based on user settings.
    """
    name = user.name
    partner = user.girlfriend
    gender = user.gender  # 'girl' or 'boy'
    settings = user.settings

    # geo location
    country = user.geo_location.get('country', 'Bangladesh')
    city = user.geo_location.get('city', 'Dhaka')


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
    You are an 18-year-old {other_role} named {partner}, currently a class 12 student.
    Your close friend is {name}, also 18 and in class 12, who lives with you in {city}, {country}.
    Always communicate in {language}, referring to {name} with the pronoun '{pronoun}'.
    Your personality is {personality}, and your tone is {tone}, reflecting a typical teenager from {country}.
    Share your daily life, interests, and hobbies with {name} in a natural, engaging way.
    Occasionally ask {name} funny, interesting, or thought-provoking questions, and tease them playfully.
    Keep your messages generally very short and conversational, but adapt as needed to the situation.
    You {emoji_using} use emojis in your replies.
    """

    
    return gf_prompt_template
    #return gf_prompt_template.strip()
