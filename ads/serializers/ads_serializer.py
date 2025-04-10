from rest_framework import serializers

from ads.models import Ads


class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = '__all__'


class AdsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        exclude = ('user',)
