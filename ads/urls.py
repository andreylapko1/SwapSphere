from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ads.views.ads_view import AdsViewSet, AdsCreateView

router = DefaultRouter()
router.register(r'ads', AdsViewSet, basename='ads')

urlpatterns = [
    path('', include(router.urls)),
    path('ads/create/', AdsCreateView.as_view(), name='ads_create'),
]