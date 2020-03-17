from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from .models import Asset, City, Country, Region, Microlocation, Currency, Property, Premises, RentRoll, OpexItem, AssetOpex
from .serializers import AssetSerializer, CitySerializer, CountrySerializer, RegionSerializer, MicrolocationSerializer, CurrencySerializer, UserSerializer, PropertySerializer, PremisesSerializer, RentRollSerializer, OpexItemSerializer, AssetOpexSerializer
from rest_framework import generics
from rest_framework import permissions
from .permissions import IsOwner, IsNotDefault, IsPropertyOwner, IsPremisesOwner, IsRentOwner
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied

#Currency Views
class CurrencyList(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class CurrencyDetail(generics.RetrieveAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

#City Views
class CityList(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class CityDetail(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

#Country Views
class CountryList(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CountryDetail(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

#Region Views
class RegionList(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class RegionDetail(generics.RetrieveAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

#Microlocation Views
class MicrolocationList(generics.ListAPIView):
    queryset = Microlocation.objects.all()
    serializer_class = MicrolocationSerializer

class MicrolocationDetail(generics.RetrieveAPIView):
    queryset = Microlocation.objects.all()
    serializer_class = MicrolocationSerializer

#User Views
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

#Asset Views
class AssetList(generics.ListCreateAPIView):
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Asset.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
class AssetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

#Property Views
class PropertyList(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Property.objects.filter(asset__owner=self.request.user)

    def perform_create(self, serializer):
        if serializer.is_valid(raise_exception=True):
            asset = serializer.validated_data['asset']
            if asset.owner != self.request.user:
                raise PermissionDenied('You dont have permissions to create property in this asset')

        serializer.save()
        

class PropertyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated, IsPropertyOwner]

class PremisesList(generics.ListCreateAPIView):
    queryset = Premises.objects.all()
    serializer_class = PremisesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Premises.objects.filter(property__asset__owner=self.request.user)

    def perform_create(self, serializer):
        if serializer.is_valid(raise_exception=True):
            asset = serializer.validated_data['property'].asset
            if asset.owner != self.request.user:
                raise PermissionDenied('You dont have permissions to create premises in this asset')
        serializer.save()

class PremisesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Premises.objects.all()
    serializer_class = PremisesSerializer
    permission_classes = [permissions.IsAuthenticated, IsPremisesOwner]

class RentRollList(generics.ListCreateAPIView):
    serializer_class = RentRollSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RentRoll.objects.filter(premises__property__asset__owner=self.request.user)

    def perform_create(self, serializer):
        if serializer.is_valid(raise_exception=True):
            asset = serializer.validated_data['premises'].property.asset
            if asset.owner != self.request.user:
                raise PermissionDenied('You dont have permissions to create premises in this asset')

        serializer.save()

class RentRollDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RentRoll.objects.all()
    serializer_class = RentRollSerializer
    permission_classes = [permissions.IsAuthenticated, IsRentOwner]

class OpexItemList(generics.ListCreateAPIView):
    queryset = OpexItem.objects.all()
    serializer_class = OpexItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OpexItem.objects.filter(Q(owner=self.request.user) | Q(default=True))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class OpexItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OpexItem.objects.all()
    serializer_class = OpexItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsNotDefault]


class OpexList(generics.ListCreateAPIView):
    queryset = AssetOpex.objects.all()
    serializer_class = AssetOpexSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AssetOpex.objects.filter(Q(property__asset__owner=self.request.user))

    def perform_create(self, serializer):
        if serializer.is_valid(raise_exception=True):
            asset = serializer.validated_data['asset']
            if asset.owner != self.request.user:
                raise PermissionDenied('You dont have permissions to add opex to this asset')

            opex_item = serializer.validated_data['opex_item']
            if (opex_item.default != True and opex_item.owner != self.request.user):
                raise PermissionDenied('You dont have permissions to use this opex item')


class OpexDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AssetOpex.objects.all()
    serializer_class = AssetOpexSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        filter = {
            'asset_owner': self.request.user,
            'pk': self.kwargs[self.lookup_field]
        }
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)

        return obj


