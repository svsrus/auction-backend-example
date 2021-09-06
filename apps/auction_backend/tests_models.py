""" Test cases for auction entities """

import datetime
from django.test import TestCase
from apps.auction_backend.models import User
from apps.auction_backend.models import Item
from apps.auction_backend.models import BidItem
from apps.auction_backend.models import AutomaticBidItem

class UserTest(TestCase):
    """ Class is responsible for testing User related entities """

    def test_create_user(self):
        """ Method tests creation of an User entity """
        user = self._create_user()
        count = len(User.objects.all())
        self.assertEqual(count, 1)

    def test_create_item(self):
        """ Method tests creation of an Item entity """
        self._create_item()
        count = len(Item.objects.all())
        self.assertEqual(count, 1)

    def test_bid_item(self):
        """ Method tests bidding of an item by a specific user """
        user = self._create_user()
        item = self._create_item()

        user.add_manual_bid(item)
        user.save()
        self.assertEqual(User.objects.get(pk=1).manual_bids.all()[0].price, 100001.50)

    def test_initialize_automatic_bid(self):
        """ Method tests initialization of automatic bid with max bid amount """
        user = self._create_user()
        user.initialize_automatic_bid(200002.50)
        user.save()
        self.assertEqual(User.objects.get(pk=3).automatic_bids.all().first().max_bid_amount, 200002.50)

    def test_set_automatic_item_bid(self):
        """ Method tests of setting of automatic bid on a selected item"""
        item = self._create_item()
        user = self._create_user()
        user.initialize_automatic_bid(1.00)
        user.set_automatic_item_bid(item)
        user.set_automatic_item_bid(item) 
        self.assertEqual(len(User.objects.get(pk=4).automatic_bids.all().first().bid_items.all()), 2)



    def _create_user(self):
        """ Private method creates User """
        user = User.objects.create(email="marco.vazquez@mail.com",
                                   password="1234567890",
                                   first_name="Marco",
                                   last_name="Vazquez",
                                   role=User.ROLE_USER)
        user.save()
        return user

    def _create_item(self):
        """ Private method creates Item """
        bidding_closure_date = datetime.date.today() + datetime.timedelta(weeks=1)
        item = Item.objects.create(name="Watch",
                                   description="Antique watch was produced in the year 1738.",
                                   current_price=100000.50,
                                   bidding_closure_date=bidding_closure_date)
        item.save()
        return item
