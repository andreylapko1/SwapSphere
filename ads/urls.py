from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ads.views.ads_view import AdsViewSet, AdsCreateView, AdsRetrieveUpdateDestroyView
from ads.views.exchange_proposal_view import ExchangeProposalCreateView, ExchangeToUserView, ExchangeConfirmView, \
    ExchangeFromMeListView

router = DefaultRouter()
router.register(r'ads', AdsViewSet, basename='ads')
router.register(r'ads/create', AdsCreateView, basename='ads_create')
router.register(r'exchange/create', ExchangeProposalCreateView, basename='exchange_create')
router.register(r'exchange/from', ExchangeFromMeListView, basename='exchange_from_me')
router.register(r'exchange/to-me', ExchangeToUserView, basename='exchange_to_user_list')
router.register(r'exchange/confirm', ExchangeConfirmView, basename='exchange_confirm')
router.register(r'ads', AdsRetrieveUpdateDestroyView, basename='ads_detail')


urlpatterns = [
    path('', include(router.urls)),
]



