from django.contrib import admin

from ads.models import ExchangeProposal, Ads


@admin.register(Ads)
class AdsAdmin(admin.ModelAdmin):
    pass


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    pass

# Register your models here.
