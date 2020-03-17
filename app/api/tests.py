from django.test import TestCase
from .models import Asset, City, Country, Region, Microlocation, Currency, Property, Premises, RentRoll
from .views import UserList
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import force_authenticate

class FillReadOnlyTestCase(TestCase):
    def setUp(self):
        #Currency
        Currency.objects.create(code='RUB', number=643, name='Российский рубль',  symbol="R")

        #Country
        Country.objects.create(name='Russia',
            currency = Currency.objects.get(code='RUB'),
            alpha2_code = 'RU',
            alpha3_code = 'RUS',
            numeric_code = 643)

        #City
        City.objects.create(name='Saint-Petersburg',
            country = Country.objects.get(alpha3_code='RUS'))

    
class AssetTestCase(APITestCase):
    def setUp(self):
        self.username_1 = "User1"
        self.email_1 = "konuchovartem@gmail.com"
        self.password_1 = "Protos93"

        self.username_2 = "User2"
        self.email_2 = "ganjasan93@gmail.com"
        self.password_2 = "1234567"

        self.user1 = User.objects.create_user(
            self.username_1, self.email_1, self.password_1
        )

        self.user2 = User.objects.create_user(
            self.username_2, self.email_2, self.password_2
        )

    def test_add_asset_with_authentiticated_user(self):
        self.client.login(username=self.username_1, password = self.password_1)

        url = reverse('asset-list')

        data = {
            "name": "Asset1",
            "fullname": "",
            "address": "",
            "city": None,
            "country": None,
            "region": None,
            "microlocation": None,
            "shape": None,
            "point": None,
            "market_value": None,
            "market_value_currency": None
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Asset.objects.count(), 1)
        self.assertEqual(Asset.objects.get().name, 'Asset1')
        self.assertEqual(Asset.objects.get().owner, self.user1)

    def test_get_asset_list_authenticated_user(self):
        #создать два ассета. Один под пользователем user1, второй под пользователем user2
        Asset.objects.create(name='Asset1', owner=self.user1).save()
        Asset.objects.create(name='Asset2', owner=self.user2).save()

        url = reverse('asset-list')

        self.client.login(username=self.username_1, password=self.password_1)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Asset1')

    def test_get_assets_authenticated_user(self):
        url = reverse('asset-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_point_add(self):
        self.client.login(username=self.username_1, password=self.password_1)
        url = reverse('asset-list')
        #send valid point
        data = {
            "name": "ValidGeoAsset",
            "point": "POINT(-95.3385 29.7245)"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Asset.objects.get().point.wkt, 'POINT (-95.3385 29.7245)')

        #send invalid point
        data = {
            "name":  "InvalidGeoAsset",
            "point": "95.1265 23.9323"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['point'][0], "Field input unrecognized as WKT, EWKT, HEXEWKB or GeoJSON.")

    def test_add_properties_auth_user(self):
        self.client.login(username=self.username_1, password=self.password_1)
        url = reverse('property-list')

        asset = Asset.objects.create(name='Asset', owner=self.user1)

        data = {
            "asset": asset.pk,
            "name": "property_1",
            "fullname": "",
            "address": "",
            "area_size": None,
            "area_unit": None,
            "book_value": None,
            "book_value_currency": None,
            "market_value": None,
            "market_value_currency": None,
            "cadastre_value": None,
            "cadastre_value_currency": None,
            "sale_date": None,
            "sale_price": None,
            "sale_currency": None,
            "cunstruction_year": None,
            "is_profitable": False
        }

        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), 1)
        self.assertEqual(Property.objects.get().name, 'property_1')
        self.assertEqual(Property.objects.get().asset, asset)

    def test_cant_get_foreign_asset(self):
        asset = Asset.objects.create(name='Asset', owner=self.user2)
        asset.save()

        url = reverse('asset-detail', args=[asset.pk])

        self.client.login(username=self.username_1, password=self.password_1)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_add_property_to_another_users_asset(self):
        asset = Asset.objects.create(name='Asset', owner=self.user2)
        asset.save()

        self.client.login(username=self.username_1, password=self.password_1)

        url = reverse('property-list')
        data = {
            "asset": asset.pk,
            "name": "property_1",
            "fullname": "",
            "address": "",
            "area_size": None,
            "area_unit": None,
            "book_value": None,
            "book_value_currency": None,
            "market_value": None,
            "market_value_currency": None,
            "cadastre_value": None,
            "cadastre_value_currency": None,
            "sale_date": None,
            "sale_price": None,
            "sale_currency": None,
            "cunstruction_year": None,
            "is_profitable": False
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Property.objects.count(), 0)

    def test_property_in_asset_view(self):
        asset = Asset.objects.create(name='Asset', owner=self.user1)
        asset.save()
        property = Property.objects.create(name='property', asset=asset).save()

        self.client.login(username=self.username_1, password=self.password_1)

        url=reverse('asset-list')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[0]['properties']), 1)


    #PREMISES TESTS
    def test_not_auth_user_cant_get_premises(self):
        #not auth user can`t get premises
        url = reverse('premises-list')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user_can_get_only_his_premises(self):
        #auth user can get only premises for his properties
        self.client.login(username=self.username_1, password=self.password_1)

        asset = Asset.objects.create(name='Asset1', owner=self.user1)
        asset.save()

        property = Property.objects.create(name='property1', asset=asset)
        property.save()

        premises = Premises.objects.create(number='1', property=property)
        premises.save()

        asset = Asset.objects.create(name='Asset2', owner=self.user2)
        asset.save()

        property = Property.objects.create(name='property2', asset=asset)
        property.save()

        premises = Premises.objects.create(number='2', property=property)
        premises.save()

        url = reverse('premises-list')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['number'], '1')

    def test_premises_show_in_property(self):
        self.client.login(username=self.username_1, password=self.password_1)

        asset = Asset.objects.create(name='Asset1', owner=self.user1)
        asset.save()

        property = Property.objects.create(name='property1', asset=asset)
        property.save()

        premises = Premises.objects.create(number='1', property=property)
        premises.save()

        url = reverse('property-detail', args=[property.pk])

        premises_url = 'http://testserver/api/v1/premises/'+str(premises.pk)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['premises']), 1)
        self.assertEqual(response.data['premises'][0], premises_url)

    def test_user_cant_get_foreign_premises(self):
        asset = Asset.objects.create(name='Asset1', owner=self.user2)
        asset.save()

        property = Property.objects.create(name='property1', asset=asset)
        property.save()

        premises = Premises.objects.create(number='1', property=property)
        premises.save()

        self.client.login(username=self.username_1, password = self.password_1)

        url = reverse('premises-detail', args=[premises.pk])

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_auth_user_cant_get_detail_premises(self):
        asset = Asset.objects.create(name='Asset1', owner=self.user2)
        asset.save()

        property = Property.objects.create(name='property1', asset=asset)
        property.save()

        premises = Premises.objects.create(number='1', property=property)
        premises.save()

        url = reverse('premises-detail', args=[premises.pk])

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_auth_user_can_get_his_premises_detail(self):
        asset = Asset.objects.create(name='Asset1', owner=self.user1)
        asset.save()

        property = Property.objects.create(name='property1', asset=asset)
        property.save()

        premises = Premises.objects.create(number='1', property=property)
        premises.save()

        url = reverse('premises-detail', args=[premises.pk])

        self.client.login(username=self.username_1, password = self.password_1)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['number'], '1')


    def test_not_auth_user_cant_add_premises(self):
        asset = Asset.objects.create(name='Asset1', owner=self.user1)
        asset.save()

        property = Property.objects.create(name='property1', asset=asset)
        property.save()

        url = reverse('premises-list')
        data = {
            "number": "1",
            "property": property.pk,
            "level": None,
            "is_leasable": False,
            "is_occupied": False,
            "area_size": None,
            "area_unit": None,
        }

        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_auth_user_can_add_premises_to_his_properties(self):
        #auth user can add premises only for his properties
        asset = Asset.objects.create(name='Asset1', owner=self.user1)
        asset.save()

        property = Property.objects.create(name='property1', asset=asset)
        property.save()

        self.client.login(username=self.username_1, password=self.password_1)

        url = reverse('premises-list')
        data = {
            "number": "1",
            "property": property.pk,
            "level": None,
            "is_leasable": False,
            "is_occupied": False,
            "area_size": None,
            "area_unit": None,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Premises.objects.count(), 1)
        self.assertEqual(Premises.objects.get().number, "1")
        self.assertEqual(Premises.objects.get().property, property)

    def test_auth_user_cant_add_premises_to_foreign_properties(self):
        asset = Asset.objects.create(name='Asset1', owner=self.user2)
        asset.save()

        property = Property.objects.create(name='property1', asset=asset)
        property.save()

        self.client.login(username=self.username_1, password=self.password_1)

        url = reverse('premises-list')
        data = {
            "number": "1",
            "property": property.pk,
            "level": None,
            "is_leasable": False,
            "is_occupied": False,
            "area_size": None,
            "area_unit": None,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    #RENTS TESTS
    def test_not_auth_user_cant_get_object_list(self):
        asset = Asset.objects.create(name='Asset1', owner=self.user2)
        asset.save()
        property = Property.objects.create(name='property1', asset=asset)
        property.save()
        premises = Premises.objects.create(number='1', property=property)
        premises.save()
        rent = RentRoll.objects.create(premises=premises).save()

        url = reverse('rent-list')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_auth_user_cant_add_object(self):
        asset = Asset.objects.create(name='Asset1', owner=self.user2)
        asset.save()
        property = Property.objects.create(name='property1', asset=asset)
        property.save()
        premises = Premises.objects.create(number='1', property=property)
        premises.save()

        url = reverse('rent-list')
        data = {
            "premises": premises.pk,
            "lease_start_date": None,
            "lease_end_date": None,
            "leased_area": None,
            "leased_area_unit": None,
            "rent": None,
            "rent_currency": None,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_auth_user_cant_get_rents_detail(self):
        asset1 = Asset.objects.create(name='Asset1', owner=self.user1)
        asset1.save()
        property1 = Property.objects.create(name='property1', asset=asset1)
        property1.save()
        premises1 = Premises.objects.create(number='1', property=property1)
        premises1.save()
        rent1 = RentRoll.objects.create(premises=premises1)
        rent1.save()

        url = reverse('rent-detail', args=[rent1.pk])

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user_can_get_only_his_rents(self):
        asset1 = Asset.objects.create(name='Asset1', owner=self.user1)
        asset1.save()
        property1 = Property.objects.create(name='property1', asset=asset1)
        property1.save()
        premises1 = Premises.objects.create(number='1', property=property1)
        premises1.save()
        rent1 = RentRoll.objects.create(premises=premises1)
        rent1.save()

        asset2 = Asset.objects.create(name='Asset1', owner=self.user2)
        asset2.save()
        property2 = Property.objects.create(name='property1', asset=asset2)
        property2.save()
        premises2 = Premises.objects.create(number='1', property=property2)
        premises2.save()
        rent2 = RentRoll.objects.create(premises=premises2)
        rent2.save()

        self.client.login(username=self.username_1, password=self.password_1)

        url = reverse('rent-list')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['premises'], premises1.pk)

    def test_auth_user_can_get_his_rents_details(self):
        asset1 = Asset.objects.create(name='Asset1', owner=self.user1)
        asset1.save()
        property1 = Property.objects.create(name='property1', asset=asset1)
        property1.save()
        premises1 = Premises.objects.create(number='1', property=property1)
        premises1.save()
        rent1 = RentRoll.objects.create(premises=premises1)
        rent1.save()

        self.client.login(username=self.username_1, password=self.password_1)

        url = reverse('rent-detail', args=[rent1.pk])

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['premises'], premises1.pk)
        

    def test_auth_user_cant_get_foreign_object_details(self):
        asset2 = Asset.objects.create(name='Asset1', owner=self.user2)
        asset2.save()
        property2 = Property.objects.create(name='property1', asset=asset2)
        property2.save()
        premises2 = Premises.objects.create(number='1', property=property2)
        premises2.save()
        rent2 = RentRoll.objects.create(premises=premises2)
        rent2.save()

        self.client.login(username=self.username_1, password=self.password_1)

        url = reverse('rent-detail', args=[rent2.pk])

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user_can_create_rent_for_his_premises(self):
        asset1 = Asset.objects.create(name='Asset1', owner=self.user1)
        asset1.save()
        property1 = Property.objects.create(name='property1', asset=asset1)
        property1.save()
        premises1 = Premises.objects.create(number='1', property=property1)
        premises1.save()

        self.client.login(username=self.username_1, password=self.password_1)

        url = reverse('rent-list')

        data = {
            "premises": premises1.pk,
            "lease_start_date": None,
            "lease_end_date": None,
            "leased_area": None,
            "leased_area_unit": None,
            "rent": None,
            "rent_currency": None,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RentRoll.objects.count(), 1)
        self.assertEqual(RentRoll.objects.get().premises, premises1)

    def test_auth_user_cant_create_rent_for_foreign_premises(self):
        asset2 = Asset.objects.create(name='Asset1', owner=self.user2)
        asset2.save()
        property2 = Property.objects.create(name='property1', asset=asset2)
        property2.save()
        premises2 = Premises.objects.create(number='1', property=property2)
        premises2.save()

        self.client.login(username=self.username_1, password=self.password_1)

        url = reverse('rent-list')

        data = {
            "premises": premises2.pk,
            "lease_start_date": None,
            "lease_end_date": None,
            "leased_area": None,
            "leased_area_unit": None,
            "rent": None,
            "rent_currency": None,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #END RENT TESTS






