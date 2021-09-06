""" Scopic Auction test cases for rest services """

import datetime
import json
from rest_framework import status
from rest_framework.test import APITransactionTestCase
from rest_framework import status
from apps.auction_backend.models import AutomaticBidItem
from apps.auction_backend.models import Item
from apps.auction_backend.models import User

SERVER_URL = "http://127.0.0.1:8000/"


class BaseViewTest(APITransactionTestCase):
    reset_sequences = True
    ROLE_USER = 2

    def setUp(self):
        """ Method sets up Item data """
        user1 = self.create_user("marco.vazquez@mail.com", "123456", "Marco", "Vazquez", BaseViewTest.ROLE_USER)
        user2 = self.create_user("jaun.perez@mail.com", "098765", "Juan", "Perez", BaseViewTest.ROLE_USER)

    def create_items(self):
        bidding_closure_date = datetime.date.today() + datetime.timedelta(weeks=1)
        self._create_item("Watch", "Antique watch was produced in the year 1738.", 100.00, bidding_closure_date)
        self._create_item("Pencil", "Antique pencil was produced in the year 1902.", 70.99, bidding_closure_date)
        self._create_item("Pen", "Antique pen was produced in the year 1857.", 68.00, bidding_closure_date)
        self._create_item("Glass", "Antique glass was found in the year 1625.", 75.50, bidding_closure_date)
        self._create_item("Fork", "Antique fork was found in the year 1688.", 50.50, bidding_closure_date)
        self._create_item("Plate", "Antique plate was found in the year 1893.", 25.00, bidding_closure_date)
        self._create_item("Chair", "Antique chair was found in the year 1933.", 35.00, bidding_closure_date)
        self._create_item("Vase", "Antique vase was found in the year 1957.", 60.00, bidding_closure_date)
        self._create_item("Painting", "Antique painting was produced in the year 1328.", 20.50, bidding_closure_date)
        self._create_item("Table", "Antique table was produced in the year 1639.", 10.00, bidding_closure_date)
        self._create_item("Carpet", "Antique carpet was produced in the year 1555.", 5.50, bidding_closure_date)
        self._create_item("Cloth", "Antique cloth was produced in the year 1482.", 1.00, bidding_closure_date)

    def create_user(self, email, password, first_name, last_name, role):
        """ Private method creates User """
        user = User.objects.create(email=email,
                                   password=password,
                                   first_name=first_name,
                                   last_name=last_name,
                                   role=role)
        user.save()
        return user

    def _create_item(self, name, description, current_price, bidding_closure_date):
        """ Private method creates Item """
        item = Item.objects.create(name=name,
                                    description=description,
                                    current_price=current_price,
                                    bidding_closure_date=bidding_closure_date)
        item.save()

class ItemViewTest(BaseViewTest):
    """ Class is responsible for testing Item related backend services """
    def setUp(self):
        super().setUp()
        super().create_items()

    def test_get_latest_items(self):
        """ Method tests latest items service """
        response = self.client.get(SERVER_URL + "api/latestItems/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 10)

    def test_get_latest_items_paginated(self):
        """ Method tests latest items with pagination service """
        request_json = { "shownItemsCount" : 10 }
        response = self.client.get(SERVER_URL + "api/latestItems/", request_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_full_search_ordered_and_paginated_items(self):
        """ Method uses search item by name, description service """
        request_json = { "shownItemsCount" : 0, 
                         "searchItemName" : "Table", 
                         "searchItemDescription" : "carpet", 
                         "orderBy" : "priceAscending"} #priceDescending
        response = self.client.get(SERVER_URL + "api/searchItems/", request_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_view_item_by_id(self):
        """ Method gets item by id service """
        request_json = { "itemId" : 12 }
        response = self.client.get(SERVER_URL + "api/item/", request_json, format='json')
        response_json = json.loads(response.content)
        response_item_id = response_json["item_id"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_item_id, 12)

    def test_create_item(self):
        """ Method posts new Item data for its creation """
        request_json = { "name" : "Spyglass", 
                         "description" : "Antique spyglass found in the year 1438", 
                         "current_price" : 998.88, 
                         "bidding_closure_date" : "2021-09-06 12:00:00"}
        response = self.client.post(SERVER_URL + "api/item/", request_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_item_with_backend_validations(self):
        """ Method posts new Item data for its creation but with errors to show validation error messages """
        request_json = { "name" : "Spyglass", 
                         "description" : "Antique spyglass found in the year 1438"}
        response = self.client.post(SERVER_URL + "api/item/", request_json, format='json')
        response_error_messages_json = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response_error_messages_json), 2)

    def test_create_bid_item(self):
        """ Method posts a bid on a selected item """
        request_json = { "userId" : 1, "itemId" : 12 }
        response = self.client.post(SERVER_URL + "api/bidItem/", request_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class AutomaticBidItemViewTest(BaseViewTest):
    """ Class is responsible for testing AutomaticBidItem related backend services """
    def setUp(self):
        super().create_items()
        user1 = super().create_user("martin.lopez@mail.com", "111111", "Martin", "Lopez", BaseViewTest.ROLE_USER)
        user2 = super().create_user("julia.rodriguez@mail.com", "222222", "Julia", "Rodriguez", BaseViewTest.ROLE_USER)
        self._create_automatic_bid_item(user1, 200.11)

    def test_get_automatic_bid_item_by_id(self):
        """ Method gets automatic bid item by id service """
        request_json = { "userId" : 1 }
        response = self.client.get(SERVER_URL + "api/automaticBidItem/", request_json, format='json')
        response_json = json.loads(response.content)
        automatic_bid_item_id = response_json["automatic_bid_item_id"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(automatic_bid_item_id, 1)

    def test_create_automatic_bid_item(self):
        """ Method posts data for Automatic Bid Item for its initialization """
        request_json = { "userId" : 2, "maxBidAmount" : 200.22}
        response = self.client.post(SERVER_URL + "api/automaticBidItem/", request_json, format='json')
        response_json = json.loads(response.content)
        automatic_bids = response_json["automatic_bids"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(automatic_bids), 1)

    def _create_automatic_bid_item(self, user, max_bid_amount):
        """ Method creates automatic bid item for a given user """
        user.initialize_automatic_bid(max_bid_amount)
        user.save()
        