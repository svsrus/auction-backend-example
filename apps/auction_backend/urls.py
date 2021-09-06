""" Module Scopic Auction Test REST URL Configuration """
from django.urls import path
from .views import LatestItemsView
from .views import SearchItemsView
from .views import ItemView
from .views import AutomaticBidItemView
from .views import BidItemView
from .views import LastBidItemUserView

urlpatterns = [
    path('latestItems/', LatestItemsView.as_view(), name="latestItemsView"),
    path('searchItems/', SearchItemsView.as_view(), name="searchItemsView"),
    path('item/', ItemView.as_view(), name="itemView"),
    path('automaticBidItem/', AutomaticBidItemView.as_view(), name="automaticBidItemView"),
    path('bidItem/', BidItemView.as_view(), name="bidItemView"),
    path('lastBidItemUser/', LastBidItemUserView.as_view(), name="lastBidItemUserView"),
]
