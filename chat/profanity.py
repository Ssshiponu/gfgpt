# English Sensitive Words
bad_words = [
    "বাইনচোদ", "গোদা", "Koromchod", "Notimagi", "Bokachoda", "Hijrachoda", "হালারপুত", 
    "Madarirput", "khankirchele", "আবালচোদা", "বোকাচোদা", "মাদারচোদ", "Bainchod", 
    "Madarchod", "মাগী", "মাগি", "চুদমারানি", "বাইঞ্চুদ", "খানকিমাগী", "harami", 
    "চুইদ্দা", "mage", "noti", "বান্দীরপোলা", "behenchod", "ছিনাল", "চুতমারানি", 
    "Notkirpu", "Chidanirpola", "Chudna", "Nanirheda", "Nanichod", "Babarchod", 
    "Emonchoda", "Chutkikhor", "Magi", "Magirdalal", "Vutkachoda", "Khankimagi", 
    "Nanarchod", "Khalarchod", "Goruchoda", "চুদিরভাই", "সাওয়াচোদা", "চুদিরভাই", 
    "Dhon", "Bal", "Chudi", "Bara", "Leora", "Voda", "Chodna", "চোদা", "Bakchod", 
    "Rendy", "Banchode", "Maagi", "Gandu", "Besshya", "Bhoda", "Chudmu", "Gud", 
    "গুদ", "Khanki", "Mang", "Naang", "ল্যাং", "Pond", "Putki", "Sudanirfua", 
    "Sutmurani", "ভুসকি", "vuski", "Bandii", "Bessha", "বেশ্যা", "chama", "ছামারপো", 
    "chamarpo", "chamarpola", "chamarfo", "ঠাপ", "chood", "চোতমারানি", "চোদ", 
    "heda", "হেডা", "হেডারপো", "হেডারপোলা", "fungi", "Futki", "haramjada", 
    "হারামজাদা", "haramjadi", "হারামজাদি", "হারামজাদী", "kuttargu", "কুত্তারগু", 
    "laora", "lerr", "Maal", "maderchood", "madarcod", "মাদারফাকার", "Nunu", 
    "pasa", "podmarani", "Suda-sudi", "SUDAURY", "SUTHH-MAROUNY", "ভোদা", "চুষে", 
    "দুদ", "পতিতা", "খানকীর", "চুদনাগিরি", "চুদা", "চুদ্দে", "খানকির", "চুদি", 
    "ভোদার", "বোকাচুদা", "মাদারচুদে", "পোন্দাইলাম", "বাইনঞ্চোদরা", "চোট্টা", 
    "হুগামারা", "চুদির", "চুদাও", "চুদ্দা", "চুদাস", "পুটকিই", "চুদাচুদি", 
    "চোদনে", "চুদেরা", "ফকিন্নিচোদারা", "মাদারিরা", "Fuck", "বোকাচোদার", 
    "পুটকি", "মাগীর", "ভাদাইমার", "খান্কির", "বোকাচোদাই", "পুটকিমারা", "আচোদা", 
    "বোকাচোদারা", "চোদায়বার", "খাংকির", "চোদাও", "বুকচুদ", "চোদার", "মাগির", 
    "পুটকির", "খানকি", "বান্দির", "পুটকিতে", "মাদারি", "ধোন", "ধন", "ভরে", 
    "ঢুকামু", "কনডম", "পাছা", "হিজরা", "পাছায়", "চুদমু", "ঢুকাইয়া", "বিচিতে", 
    "হিজড়া", "বাইঞ্চোদ", "চুদানির", "নটি", "ভোদায়", "নুনু", "পলা", "লেউরা", 
    "ল্যাওড়া", "হোল", "ভুস্কি", "নটির", "চোদন", "কন্ডম", "মাঙ্গি", "পোলায়", 
    "পোলা।", "বাইন্দা", "পুট", "চুদানি", "লাগায়া", "চোদনা", "চোদে", "ফালাইয়া", 
    "ভিত্রে", "লেংটা", "হিজলা", "মাঙ্গির", "মাইন্দার", "পোদ", "চুতমারানির", 
    "মাদারচুদ", "মাদারটোস্ট", "পুতকি", "সেক্স", "চুদন", "চুইদা", "বেইসশা", 
    "খাঙ্কি", "লাগাই", "পোলার", "চো", "লাগাইয়া", "সোদনে", "ফালামু", "সোদন", 
    "ডুকামু", "পুকটি", "দুদের", "লাগায়", "চোদনার", "মাদারটোষ্ট", "পুতকির", 
    "চুদনা", "চুদনার", "ঢুকাই", "হোগামারা", "খাঙ্কির", "হাগাই", "নাটকির", 
    "বুদা", "চুদ্মু", "খানকিরপোলা", "মাইন্দারের", "পুটু", "ভইড়া", "হারামি", 
    "হাারামজাদা", "হারামখোর", "পাছা-মারা", "বানচোত", "পেদামু", "ভোদাই", 
    "পুটকি-মারা", "লেদানি", "খবিশ", "চুদা-খা", "লেওরা", "ল্যাদানী", "baincod", 
    "sumondi", "goda", "halarput", "abalcoda", "bokacoda", "itjadi", "cudmarani", 
    "manggu", "baincud", "cuidda", "bandirpola", "chinal", "cutmarani", "cudhirvai", 
    "saoyacoda", "cudirvai", "cuda", "cudde", "acuda", "oshlil", "cod", "kamlacuda", 
    "cudi", "vodar", "cude", "bokacuda", "heta", "madarcude", "pondailam", "bainoncodra", 
    "cotta", "hugamara", "cudir", "cudao", "cudda", "cudas", "putkii", "cudacudi", 
    "codne", "cudera", "fkinnicodara", "madarira", "bokacodar", "beshja", "codao", 
    "bukcud", "codar", "bukana", "ljangta", "put", "bici", "putkir", "bandir", 
    "putkite", "madari", "vre", "dhukamu", "konodom", "pacha", "hijra", "pachay", 
    "cudmu", "dhukaiya", "bicite", "cudanir", "nti", "voday", "pla", "leura", 
    "ljaora", "hol", "ntir", "codon", "kondom", "manggi", "polay", "pola.", "bainda", 
    "cudani", "lagaya", "codna", "code", "falaiya", "vitre", "lengta", "hijla", 
    "manggir", "maindar", "pod", "cutmaranir", "madarcud", "madartost", "seks", 
    "cudon", "cuida", "beissha", "khangki", "lagai", "polar", "lagaiya", "sodne", 
    "falamu", "sodon", "dukamu", "pukti", "duder", "lagay", "codnar", "madartosht", 
    "cudna", "cudnar", "hagai", "natkir", "khankirpola", "maindarer", "putu", 
    "haaramjada", "haramkhor", "bancot", "pedamu", "vodai", "putki-mara", "khbish", 
    "cuda-kha", "maigja", "ljadani"
]

def check_profanity(text):
    """
    Check if the input text contains any profane word or phrase.
    
    Args:
        text (str): The input word or phrase to check.
    
    Returns:
        bool: True if profanity is found, else False
        list: List of matched profane words/phrases
    """
    text = str(text).lower()
    matched = []

    for bad in bad_words:
        if bad.lower() in text.split(" "):
            matched.append(bad)
            print(matched)
    return (len(matched) > 0), matched
