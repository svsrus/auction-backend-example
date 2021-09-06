""" Scopic Auction Test module for Model Serializers to JSON/XML format """
import datetime
import pytz
from datetime import datetime
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ModelField
from rest_framework.serializers import RelatedField
from rest_framework.serializers import DateTimeField
from rest_framework.serializers import ValidationError
from .models import User
from .models import Item
from .models import AutomaticBidItem
from .models import BidItem

class AutomaticBidItemSerializer(ModelSerializer):
    """ AutomaticBidItem entity Serializer """
    class Meta:
        model = AutomaticBidItem
        fields = ["automatic_bid_item_id", "max_bid_amount"]

class UserSerializer(ModelSerializer):
    """ User entity Serializer """
    automatic_bids = AutomaticBidItemSerializer(required=False, many=True)

    class Meta:
        model = User
        fields = ["user_id", "first_name", "last_name", "automatic_bids"]

class BidItemSerializer(ModelSerializer):
    """ BidItem entity Serializer """
    date = DateTimeField(required=False, format="%Y-%m-%d %H:%M:%S")
    user = UserSerializer(required=False, many=False)

    class Meta:
        model = BidItem
        fields = ["bid_item_id", "price", "date", "automatic", "user"]

class ItemSerializer(ModelSerializer):
    """ Item entity Serializer """
    bidding_closure_date = DateTimeField(required=True, format="%Y-%m-%d %H:%M:%S")
    bids = BidItemSerializer(required=False, many=True)

    class Meta:
        model = Item
        fields = ["item_id", "name", "description", "current_price", "bidding_closure_date", "bids"]

    def validate_bidding_closure_date(self, bidding_closure_date):
        """ Method validates if bidding closure date is greater then today. Only for testing the default UTC is used. """
        bidding_closure_date_utc = bidding_closure_date.replace(tzinfo=pytz.UTC)
        today_datetime_utc = datetime.today().replace(tzinfo=pytz.UTC) 
        if bidding_closure_date_utc <= today_datetime_utc:
            raise ValidationError("Bidding closure date must be at least the next day from today.")
        return bidding_closure_date
        