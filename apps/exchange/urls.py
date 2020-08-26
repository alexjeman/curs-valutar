from django.urls import path

from apps.exchange.views import BankListView, CoinListView, RateListView, RatesPredictionListView

urlpatterns = [
    path('banks/', BankListView.as_view(), name='banks'),
    path('coins/', CoinListView.as_view(), name='coins'),
    path('rates/', RateListView.as_view(), name='rates'),
    path('prediction/', RatesPredictionListView.as_view(), name='rates_prediction'),
]
