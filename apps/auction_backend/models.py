from django.db import models

from decimal import Decimal
from django.db.models import Model
from django.db.models import AutoField
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import DecimalField
from django.db.models import EmailField
from django.db.models import IntegerField
from django.db.models import ForeignKey
from django.db.models import ManyToManyField

class User(Model):
    """ User entity holds information for different types of users """
    LAST_USER_BID_ITEM_SQL = "SELECT u.user_id, bi.bid_item_id " + \
                             "FROM auction_backend_user as u " + \
                             "INNER JOIN auction_backend_automaticbiditem as abi ON u.user_id = abi.user_id " + \
                             "INNER JOIN auction_backend_automaticbiditem_bid_items as abibi ON abi.automatic_bid_item_id = abibi.automaticbiditem_id " + \
                             "INNER JOIN auction_backend_biditem as bi ON abibi.biditem_id = bi.bid_item_id " + \
                             "WHERE bi.item_id=%s " + \
                             "UNION " + \
                             "SELECT u.user_id, bi.bid_item_id " + \
                             "FROM auction_backend_user as u " + \
                             "INNER JOIN auction_backend_biditem as bi ON u.user_id = bi.user_id " + \
                             "WHERE bi.item_id=%s " + \
                             "ORDER BY bid_item_id DESC;"
    ROLE_ADMIN = 1
    ROLE_USER = 2
    USER_ROLES = [
        (ROLE_ADMIN, 'Administrator role'),
        (ROLE_USER, 'User role')
    ]

    user_id = AutoField(primary_key=True)
    email = EmailField(null=True, blank=False, max_length=255)
    password = CharField(null=True, blank=False, max_length=255) #TODO must be one way encrypted
    first_name = CharField(null=True, blank=False, max_length=128)
    last_name = CharField(null=True, blank=False, max_length=128)
    role = IntegerField(null=True, blank=False, choices=USER_ROLES)

    def add_manual_bid(self, item):
        """ Method adds new BidItem to the manual_bids list """
        item.current_price += 1
        item.save()
        manual_bid_item = BidItem.objects.create(user=self, 
                                                 item=item, 
                                                 price=item.current_price)
        manual_bid_item.save()
        self.manual_bids.add(manual_bid_item)

    def initialize_automatic_bid(self, max_bid_amount):
        """ Method initializes AutomaticBidItem for futher execution of automatic bids """
        if (not self.automatic_bids.exists()):
            automatic_bid_item = AutomaticBidItem.objects.create(user=self, max_bid_amount=max_bid_amount)
            self.automatic_bids.add(automatic_bid_item)
        else:
            automatic_bid_item = self.automatic_bids.all().first()
            automatic_bid_item.max_bid_amount = max_bid_amount
            automatic_bid_item.bid_items.clear()
            automatic_bid_item.save()

    def set_automatic_item_bid(self, item):
        """ Method creates/sets AutomaticBidItem with the Item to execute future automatic bids """
        automatic_bid_item = self.automatic_bids.all().first()
        bid_item = BidItem.objects.create(user=self, 
                                            item=item, 
                                            price=item.current_price+1,
                                            automatic=True)
        
        bid_item.save()
        automatic_bid_item.bid_items.add(bid_item)
        automatic_bid_item.max_bid_amount -=1
        automatic_bid_item.save()
        item.current_price += 1
        item.save()

class Item(Model):
    """ Item entity holds information for item that is used for bidding """
    item_id = AutoField(primary_key=True)
    name = CharField(max_length=128)
    description = CharField(max_length=255)
    current_price = DecimalField(max_digits=19, decimal_places=2)
    bidding_closure_date = DateTimeField(blank=True, null=True)

class BidItem(Model):
    """ BidItem entity holds information of a bid on an specific item """
    bid_item_id = AutoField(primary_key=True)
    user = ForeignKey(User, on_delete=models.CASCADE, related_name="manual_bids")
    item = ForeignKey(Item, on_delete=models.CASCADE, related_name="bids")
    price = DecimalField(max_digits=19, decimal_places=2)
    date = DateTimeField(auto_now_add=True, blank=True, null=True)
    automatic = BooleanField(null=False, default=False)    

class AutomaticBidItem(Model):
    """ AutomaticBidItem entity holds information to auto-execute bids on an specific item """
    USER_AUTOMATIC_BID_ITEM_SQL = "SELECT abi.automatic_bid_item_id, abi.max_bid_amount, abi.user_id " + \
                                  "FROM auction_backend_automaticbiditem as abi " + \
                                  "WHERE abi.user_id=%s"
    automatic_bid_item_id = AutoField(primary_key=True)
    user = ForeignKey(User, on_delete=models.CASCADE, related_name="automatic_bids")
    bid_items = ManyToManyField(BidItem, blank=True)
    max_bid_amount = DecimalField(max_digits=19, decimal_places=2)

    def add_automatic_item_bid(self, bid_item):
        """ Method adds new auto bidding item if the max bid amount is a given bid item price """
        if (Decimal(self.max_bid_amount) > Decimal(bid_item.price)):
            self.max_bid_amount = Decimal(self.max_bid_amount) - Decimal(bid_item.price)
            self.bid_items.add(bid_item)


