""" Scopic Auction Test - views module """

from decimal import Decimal
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Item
from .models import User
from .models_serializers import AutomaticBidItemSerializer
from .models_serializers import ItemSerializer
from .models_serializers import UserSerializer
from .threads import AutomaticBidItemThread

PAGE_SIZE = 10

class BaseView(APIView):
    def get_request_get_int(self, request, key):
        """ Method looks for a given INT attribute in a GET request data and returns its value """
        return int(request.GET.get(key)) if key in request.GET else 0

    def get_request_get_string(self, request, key):
        """ Method looks for a given STR attribute in a GET request data and returns its value """
        return request.GET.get(key) if key in request.GET else ""

    def get_request_post_string(self, request, key):
        """ Method looks for a given STR attribute in a PUT/POST request data and returns its value """
        return request.data[key] if key in request.data else ""

    def get_request_post_int(self, request, key):
        """ Method looks for a given INT attribute in a PUT/POST request data and returns its value """
        return int(request.data[key]) if key in request.data else 0

    def get_request_post_decimal(self, request, key):
        """ Method looks for a given DECIMAL attribute in a PUT/POST request data and returns its value """
        return Decimal(request.data[key]) if key in request.data else 0

class BaseItemsView(BaseView):
    def get_order_attribute(self, request):
        """ Method returns order by attribute name """
        if ("orderBy" in request.GET) :
            if (request.GET.get("orderBy") == "priceAscending"):
                return "current_price"
            elif (request.GET.get("orderBy") == "priceDescending"):
                return "-current_price"
        return "-item_id" #Default

class LatestItemsView(BaseItemsView):
    def get(self, request):
        """ Method retrieves lastest published items and returns this list as JSON """
        last_row = super().get_request_get_int(request, "shownItemsCount")
        items = Item.objects.all().order_by(super().get_order_attribute(request))[last_row:last_row + PAGE_SIZE]
        item_serializer = ItemSerializer(items, many=True)
        items_json = item_serializer.data
        return Response(items_json)

class SearchItemsView(BaseItemsView):
    def get(self, request):
        """ Method searches lastest published items and returns this list as JSON """
        search_item_name = super().get_request_get_string(request, "searchItemName")
        search_item_description = super().get_request_get_string(request, "searchItemDescription")
        last_row = super().get_request_get_int(request, "shownItemsCount")
        items = self._filter_items(request, search_item_name, search_item_description, last_row)
        item_serializer = ItemSerializer(items, many=True)
        items_json = item_serializer.data
        return Response(items_json)

    def _filter_items(self, request, search_item_name, search_item_description, last_row):
        #TODO Pass to Service Layer and change to strategy pattern
        if (search_item_name and not search_item_description):
            return Item.objects.filter(name__icontains=search_item_name) \
                                       .order_by(super().get_order_attribute(request))[last_row:last_row + PAGE_SIZE]
        elif (not search_item_name and search_item_description):
            return Item.objects.filter(description__icontains=search_item_description) \
                                       .order_by(super().get_order_attribute(request))[last_row:last_row + PAGE_SIZE]
        elif (search_item_name and search_item_description):
            return Item.objects.filter(Q(name__icontains=search_item_name) | 
                                       Q(description__icontains=search_item_description)) \
                                       .order_by(super().get_order_attribute(request))[last_row:last_row + PAGE_SIZE]

class ItemView(BaseView):
    def get(self, request):
        """ Method retrieves a selected Item it as JSON """
        item_id = super().get_request_get_int(request, "itemId")
        item = Item.objects.get(pk=item_id)
        item_serializer = ItemSerializer(item)
        item_json = item_serializer.data
        return Response(item_json)

    def post(self, request):
        """ Method saves new Item """
        item_serializer = ItemSerializer(data=request.data)
        if item_serializer.is_valid():
            item_serializer.save()
            return Response(item_serializer.data, status=status.HTTP_201_CREATED)
        return Response(item_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class BidItemView(BaseView):
    def post(self, request):
        """ Method retrieves a selected Item """
        user = User.objects.get(pk=super().get_request_post_int(request, "userId"))
        item = Item.objects.get(pk=super().get_request_post_int(request, "itemId"))
        if (user and item):
            user.add_manual_bid(item)
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class LastBidItemUserView(BaseView): 
    def get(self, request):
        """ Method retrieves Last bid item user as JSON """
        item_id = super().get_request_get_int(request, "itemId")
        item_bid_users = User.objects.raw(User.LAST_USER_BID_ITEM_SQL, [item_id, item_id])
        if (len(item_bid_users) > 0):
            last_bid_item_user = User.objects.get(pk=item_bid_users[0].user_id)
            user_serializer = UserSerializer(last_bid_item_user)
            user_json = user_serializer.data
            return Response(user_json)
        return Response(status=status.HTTP_404_NOT_FOUND)
    

class AutomaticBidItemView(BaseView):
    def get(self, request):
        """ Method retrieves AutomaticBidItem as JSON """
        user = User.objects.get(pk=super().get_request_get_int(request, "userId"))
        automatic_bid_item_serializer = AutomaticBidItemSerializer(user.automatic_bids.all().first())
        automatic_bid_item_serializer_json = automatic_bid_item_serializer.data
        return Response(automatic_bid_item_serializer_json)

    def put(self, request):
        """ Method start AutomaticBidItemThread to make auto bidding """
        user = User.objects.get(pk=super().get_request_post_int(request, "userId"))
        item = Item.objects.get(pk=super().get_request_post_int(request, "itemId"))
        if (user and item):
            automaticBidItemThread = AutomaticBidItemThread(user.user_id, item.item_id)
            automaticBidItemThread.start()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """ Method creates new automatic bid configuration """
        user = User.objects.get(pk=super().get_request_post_int(request, "userId"))
        max_bid_amount = super().get_request_post_decimal(request, "maxBidAmount")

        if user is not None and max_bid_amount is not None:
            user.initialize_automatic_bid(max_bid_amount)
            user.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
