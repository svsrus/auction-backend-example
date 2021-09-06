""" Scopic Auction Test - threading module """

import time
from threading import Lock
from threading import Thread
from django.db import connection
from .models import AutomaticBidItem
from .models import Item
from .models import User

class AutomaticBidItemThread(Thread):
    """ Automatic bidding thread per user and item """

    def __init__(self, user_id, item_id):
        """ Initialization of local attributes """
        Thread.__init__(self, name="Thread for the user_id = '" + str(item_id) + "'")
        self.user_id = user_id
        self.item_id = item_id
        self.lock = Lock()

    def run(self):
        """ Run method executes until all the money is spend on selected item """
        """ No checking for bidding closure date is done, due to lack of time to code it """

        max_bid_amount = 0
        print("STARTING - " + super().name) #TODO change to logger
        with self.lock:
            max_bid_amount = self._get_max_bid_amount()

        while(max_bid_amount > 0):
            print("RUNNING " + super().name) #TODO change to logger
            with self.lock:
                user = User.objects.get(pk=self.user_id)
                item_bid_users = User.objects.raw(User.LAST_USER_BID_ITEM_SQL, [self.item_id, self.item_id])

                print("USER_ID = " + str(user.user_id) + " LAST_BID_ITEM_USER_ID = " + str(item_bid_users[0].user_id)) #TODO change to logger
                """ If the last bid is not made by this user then make an automatic bid """
                if (len(item_bid_users) > 0 and item_bid_users[0].user_id != user.user_id):
                    user.set_automatic_item_bid(Item.objects.get(pk=self.item_id))
                
                max_bid_amount = self._get_max_bid_amount()
                time.sleep(1)
        
        print("FINISHING - " + super().name) #TODO change to logger

    def _get_max_bid_amount(self):
        """ Method searches for the max bid amount for a given user """
        max_bid_amount = 0
        automatic_bid_item = AutomaticBidItem.objects.raw(AutomaticBidItem.USER_AUTOMATIC_BID_ITEM_SQL, [self.user_id])
        if (len(automatic_bid_item) > 0):
            max_bid_amount = automatic_bid_item[0].max_bid_amount
        return max_bid_amount

