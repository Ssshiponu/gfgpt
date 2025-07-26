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

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return f'name: {self.name}, girlfriend: {self.girlfriend}'