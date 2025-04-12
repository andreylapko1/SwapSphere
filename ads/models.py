from django.contrib.auth.models import User
from django.db import models


class Ads(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Новый'),
        ('used', 'Б/У'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField()
    image_url = models.ImageField(null=True, blank=True)
    category = models.CharField(max_length=120)
    condition = models.CharField(max_length=120, choices=CONDITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ExchangeProposal(models.Model):

    STATUS_CHOICES = (
       ( 'ожидает', 'Ожидает'),
        ('принята', 'Принята'),
        ('отклонена', 'Отклонена'),
    )

    ad_sender = models.ForeignKey(Ads, on_delete=models.CASCADE, related_name='ad_sender')
    ad_receiver = models.ForeignKey(Ads, on_delete=models.CASCADE, related_name='ad_receiver')
    comment = models.CharField(max_length=120)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default='ожидает')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From {self.ad_sender.title} to {self.ad_receiver.title}'


# Create your models here.
