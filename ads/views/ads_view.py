from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, \
    RetrieveModelMixin
from rest_framework.viewsets import ViewSet, GenericViewSet, ModelViewSet
from ads.models import Ads
from ads.permissions import IsOwnerOrReadOnly
from ads.serializers import AdsSerializer
from ads.serializers.ads_serializer import AdsCreateSerializer


class AdsViewSet(ListModelMixin, GenericViewSet):
    filter_backends = (DjangoFilterBackend,OrderingFilter, SearchFilter)
    search_fields = ('title','description')
    ordering_fields = ['category', 'condition']
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer


class AdsCreateView(GenericViewSet, CreateModelMixin):
    queryset = Ads.objects.all()
    serializer_class = AdsCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AdsRetrieveUpdateDestroyView(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = AdsSerializer


    def get_object(self):
        return Ads.objects.get(pk=self.kwargs['pk'])
