from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('assets/', AssetList.as_view(), name='asset-list'),
    path('assets/<int:pk>/', AssetDetail.as_view(), name='asset-detail'),
    path('properties/', PropertyList.as_view(), name='property-list'),
    path('properties/<int:pk>', PropertyDetail.as_view(), name='property-detail'),
    path('premises/', PremisesList.as_view(), name='premises-list'),
    path('premises/<int:pk>', PremisesDetail.as_view(), name='premises-detail'),
    path('rents/', RentRollList.as_view(), name='rent-list'),
    path('rents/<int:pk>', RentRollDetail.as_view(), name='rent-detail'),
    path('cities/', CityList.as_view(), name='city-list'),
    path('cities/<int:pk>/', CityDetail.as_view(), name='city-detail'),
    path('countries/', CountryList.as_view(), name='country-list'),
    path('countries/<int:pk>/', CountryDetail.as_view(), name='country-detail'),
    path('regions/', RegionList.as_view(), name='region-list'),
    path('regions/<int:pk>/', RegionDetail.as_view(), name='region-detail'),
    path('microlocations/', MicrolocationList.as_view(), name='microlocation-list'),
    path('microlocations/<int:pk>/', MicrolocationDetail.as_view(), name='microlocation-detail'),
    path('currencies/', CurrencyList.as_view(), name='currencie-list'),
    path('currencies/<int:pk>/', CurrencyDetail.as_view(), name='currencie-detail'),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('opex_items/', OpexItemList.as_view(), name='opexitem-list'),
    path('opex_items/<int:pk>/', OpexItemDetail.as_view(), name='opexitem-detail'),
    path('opex/', OpexList.as_view(), name='opex-list'),
    path('opex/<int:pk>/', OpexDetail.as_view(), name='opex-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)