from django.db import models

class Usr(models.Model):
    languages = [
        'auto',
        'বাংলা',
        'Banglish',
        'English',
        'हिंदी',
        'Hinglish',
    ]

    use_emojis = [
        'auto',
        'yes',
        'no',
    ]

    pronouns = {
        'auto': ['you',],
        'বাংলা': ['তুমি', 'তুই', 'আপনি'],
        'Banglish': ['tumi', 'tui', 'apni'],
        'English': ['you',],
        'हिंदी': ['तुम', 'तू', 'आप'],
        'Hinglish': ['tum', 'tu', 'aap'],
    }

    personalities = [
        'friendly',
        'respectful',
        'responsive',
    ]

    tones = [
        'romantic',
        'flirty',
        'funny',
        'serious',
        'sad',
        'angry',
        'helpful',
    ]

    genders = (
        ("boy", "Boy"),
        ("girl", "Girl"),
    )

    def default_usr_settings():
        return {
            "language": 'auto',
            "use_emojis": 'auto',
            "pronoun": 'you',
            "personality": 'friendly',
            "tone": 'romantic',
        }

    session = models.CharField(max_length=100)
    messages = models.JSONField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    girlfriend = models.CharField(max_length=100, null=True, blank=True)

    gender = models.CharField(max_length=100, null=True, blank=True , choices=genders)

    # settings
    settings = models.JSONField(default= default_usr_settings)

    # tracking
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    geo_location = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return f'name: {self.name}, girlfriend: {self.girlfriend}'
    
class APIKey(models.Model):
    key = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = 'API Key'
        verbose_name_plural = 'API Keys'
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.key
    
class APIRequest(models.Model):
    '''
    A model to track gemini API requests
    '''
    usr = models.ForeignKey(Usr, null=True, on_delete=models.SET_NULL, related_name='api_requests')

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    api_key_index = models.IntegerField(default=0)
    model_name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = 'API Request'
        verbose_name_plural = 'API Requests'
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return f'IP:{self.ip_address}, KEY:{self.api_key_index}, MODEL:{self.model_name}'
    
class SEO(models.Model):
    name = models.CharField(max_length=100)
    altname = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    keywords = models.TextField()
    author = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = 'SEO'
        verbose_name_plural = 'SEO'
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.title
    
