from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Asset, City, Country, Region, Microlocation, Currency, Property, Premises, RentRoll, OpexItem, AssetOpex
from rest_framework.reverse import reverse
from django.contrib.gis.geos import GEOSGeometry


class AssetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    properties = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='property-detail')
   


    def validate_point(self, value):
        if value:
            try:
                GEOSGeometry(value)
            except:
                raise serializers.ValidationError("Field input unrecognized as WKT, EWKT, HEXEWKB or GeoJSON.")
      
        return value

    def validate_shape(self, value):
        if value:
            try:
                GEOSGeometry(value)
            except:
                raise serializers.ValidationError("Field input unrecognized as WKT, EWKT, HEXEWKB or GeoJSON.")

        return value        

    class Meta:
        model = Asset
        fields = ['id', 'owner', 'name', 'fullname', 'address', 'city', 'country', 'region', 'microlocation', 'shape', 'point', 'market_value', 'market_value_currency', 'properties']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'country', 'shape']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'currency', 'alpha2_code', 'alpha3_code', 'shape']

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'country', 'shape']

class MicrolocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Microlocation
        fields = ['name', 'description', 'country', 'city', 'shape']

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name', 'symbol']

class UserSerializer(serializers.ModelSerializer):
    assets = serializers.PrimaryKeyRelatedField(many=True, queryset=Asset.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'assets']

class PropertySerializer(serializers.ModelSerializer):
    premises = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='premises-detail')
    GLA = serializers.ReadOnlyField(source='gla')
    vacant_area = serializers.ReadOnlyField()
    NLA = serializers.ReadOnlyField(source='nla')
    OPEX = serializers.ReadOnlyField(source='opex')
    vacancy_rate = serializers.ReadOnlyField()
    gross_rental_income = serializers.ReadOnlyField()
    NOI = serializers.ReadOnlyField(source='noi')

    class Meta:
        model = Property
        fields = ['id','asset', 'name', 'fullname', 'address', 'area_size', 'area_unit', 'book_value', 'book_value_currency', 'market_value', 
                    'market_value_currency', 'cadastre_value', 'cadastre_value_currency', 'sale_date', 'sale_price', 'sale_currency', 'cunstruction_year', 
                    'is_profitable', 'GLA', 'vacant_area', 'NLA', 'OPEX', 'vacancy_rate', 'gross_rental_income', 'NOI', 'premises'] 

class PremisesSerializer(serializers.ModelSerializer):
    rents = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='rent-detail')

    class Meta:
        model = Premises
        fields = ['id', 'number', 'property', 'level', 'is_leasable', 'is_occupied', 'area_size', 'area_unit', 'rents']

class RentRollSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentRoll
        fields = ['id', 'premises', 'lease_start_date', 'lease_end_date', 'leased_area', 'leased_area_unit', 'rent', 'rent_currency']

class OpexItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpexItem
        fields = ['name', 'fullname']

class AssetOpexSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetOpex
        fields = ['property', 'opex_item', 'start_date', 'end_date', 'vat', 'montly_value', 'currency']


