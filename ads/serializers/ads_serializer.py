from rest_framework import serializers

from ads.models import Ads


class AdsSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Ads
        exclude = ['user']

    def get_username(self, obj):
        return obj.user.username

class AdsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        exclude = ('user',)

class AdsRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = '__all__'
