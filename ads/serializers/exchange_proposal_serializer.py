from rest_framework import serializers
from ads.models import ExchangeProposal, Ads


class ExchangeCreateSerializer(serializers.ModelSerializer):
    ad_sender = serializers.PrimaryKeyRelatedField(queryset=Ads.objects.none())
    ad_receiver = serializers.PrimaryKeyRelatedField(queryset=Ads.objects.none())
    class Meta:
        model = ExchangeProposal
        exclude = ('status',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user

        self.fields['ad_receiver'].queryset = Ads.objects.exclude(user=user)
        self.fields['ad_sender'].queryset = Ads.objects.filter(user=user)


class ExchangeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = '__all__'


class ExchangeConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = '__all__'