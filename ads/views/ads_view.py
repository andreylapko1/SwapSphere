from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ViewSet, GenericViewSet, ModelViewSet
from ads.models import Ads
from ads.serializers import AdsSerializer
from ads.serializers.ads_serializer import AdsCreateSerializer


class AdsViewSet(ListModelMixin, GenericViewSet):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer


class AdsCreateView(CreateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsCreateSerializer