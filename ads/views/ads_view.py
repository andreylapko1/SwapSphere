from django.http import Http404
from pyexpat.errors import messages
from rest_framework import status
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, \
    RetrieveModelMixin
from rest_framework.response import Response
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
        return get_object_or_404(Ads, pk=self.kwargs['pk'])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Success deleted"}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "message": "Ad updated successfully",
            "updated_ad": serializer.data}, status=status.HTTP_200_OK)

