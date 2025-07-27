from django.db import models

# Create your models here.

class Msg(models.Model):
    session = models.CharField(max_length=100)
    msg = models.JSONField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    girlfriend = models.CharField(max_length=100, null=True, blank=True)
    genders = (
        ("boy", "Boy"),
        ("girl", "Girl"),
    )
    gender = models.CharField(max_length=100, null=True, blank=True , choices=genders)

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