from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from ads.models import ExchangeProposal
from ads.serializers.exchange_proposal_serializer import ExchangeCreateSerializer, ExchangeListSerializer, \
    ExchangeConfirmSerializer


class ExchangeProposalCreateView(GenericViewSet, CreateModelMixin):
    serializer_class = ExchangeCreateSerializer
    queryset = ExchangeProposal.objects.all()


class ExchangeToUserView(GenericViewSet, ListModelMixin):
    serializer_class = ExchangeListSerializer
    ordering_fields = ['ad_receiver', 'created_at', 'status']

    def get_queryset(self):
        return ExchangeProposal.objects.filter(ad_receiver__user=self.request.user)

class ExchangeFromMeListView(GenericViewSet, ListModelMixin):
    serializer_class = ExchangeListSerializer

    def get_queryset(self):
        return ExchangeProposal.objects.filter(ad_sender__user=self.request.user)


class ExchangeConfirmView(RetrieveModelMixin, GenericViewSet):
    serializer_class = ExchangeConfirmSerializer

    @action(detail=True, methods=['get'])
    def confirm_exchange(self, request, pk=None):
        exchange_proposal = self.get_object()

        if exchange_proposal.ad_receiver.user != request.user:
            raise PermissionDenied("You do not have permission to confirm this exchange.")

        exchange_proposal.status = 'принята'
        exchange_proposal.save()
        return Response({"status": "confirmed"}, status=status.HTTP_200_OK)


    def get_object(self):
        exchange_proposal = ExchangeProposal.objects.get(pk=self.kwargs['pk'])
        if exchange_proposal.ad_receiver.user != self.request.user:
            raise PermissionDenied("You do not have permission to confirm this exchange.")

        return exchange_proposal