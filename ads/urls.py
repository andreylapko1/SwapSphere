from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ads.views.ads_view import AdsViewSet, AdsCreateView, AdsRetrieveUpdateDestroyView

router = DefaultRouter()
router.register(r'ads', AdsViewSet, basename='ads')
router.register(r'ads/create', AdsCreateView, basename='ads_create')
router.register(r'ads', AdsRetrieveUpdateDestroyView, basename='ads_detail')


urlpatterns = [
    path('', include(router.urls)),
]


# Если тебе нужно отдельное представление для детализированного объекта
