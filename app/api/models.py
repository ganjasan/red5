from django.db import models
from django.utils import timezone
from django.contrib.gis.db import models as geomodels
from django.db.models import Q


class Currency(models.Model):   
    code = models.CharField(max_length=3, help_text="ISO3 Currency code")
    #number = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=250)
    symbol = models.CharField(max_length=10, null=True)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=250)
    currency = models.ForeignKey(Currency, on_delete= models.PROTECT, related_name="+")
    alpha2_code = models.CharField(max_length=2, null=True, blank=True, help_text='ISO2 country code')
    alpha3_code = models.CharField(max_length=3, null=True, blank=True, help_text='ISO3 country code')
    numeric_code = models.IntegerField(null=True, blank=True)
    shape = geomodels.PolygonField(null=True, blank=True)
    point = geomodels.PointField(null=True, blank=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=250)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="+")
    shape = geomodels.PolygonField(null=True, blank=True)
    point = geomodels.PointField(null=True, blank=True)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=250)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="+")
    shape = geomodels.PolygonField(null=True, blank=True)
    point = geomodels.PointField(null=True, blank=True)

    def __str__(self):
        return self.name

class Microlocation(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="+")
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="+")
    shape = geomodels.PolygonField(null=True, blank=True)
    point = geomodels.PointField(null=True, blank=True)

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=250)
    fullname = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class AssetClass(models.Model):
    name = models.CharField(max_length=80)
    definition = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Segment(models.Model):
    name = models.CharField(max_length=80)
    definition = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Asset(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        'auth.User',
        related_name='assets',
        on_delete=models.PROTECT,
    )
    name = models.CharField(max_length=250)
    fullname = models.CharField(max_length=250, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True, blank=True)
    microlocation = models.ForeignKey(Microlocation, on_delete=models.PROTECT, null=True, blank=True)
    asset_class = models.ForeignKey(AssetClass, on_delete=models.PROTECT, null=True, blank=True)
    segment = models.ForeignKey(Segment, on_delete=models.PROTECT, null=True, blank=True)
    shape = geomodels.PolygonField(null=True, blank=True)
    point = geomodels.PointField(null=True, blank=True)
    market_value = models.BigIntegerField(null=True, blank=True)
    market_value_currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="+", null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted = models.DateTimeField(blank=True, null=True)



    def __str__(self):
        return self.name

class Property(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='properties')
    name = models.CharField(max_length=250)
    fullname = models.CharField(max_length=250, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    area_size = models.FloatField(null=True, blank=True)
    area_unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name="+", null=True, blank=True)
    book_value = models.BigIntegerField(null=True, blank=True) 
    book_value_currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="+", null=True, blank=True) #
    market_value = models.BigIntegerField(null=True, blank=True)
    market_value_currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="+", null=True, blank=True)
    cadastre_value = models.BigIntegerField(null=True, blank=True)
    cadastre_value_currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="+", null=True, blank=True)
    sale_date = models.DateField(null=True, blank=True)
    sale_price = models.BigIntegerField(null=True, blank=True)
    sale_currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="+", null=True, blank=True)
    cunstruction_year = models.IntegerField(null=True, blank=True)
    is_profitable = models.BooleanField(null=True, blank=True)
    
    @property
    def gla(self):
        """Gross Lease Area - calculated from premises leasable area """
        return sum(list(map(lambda p: p.area_size, self.premises.filter(is_leasable=True))))

    @property
    def vacant_area(self):
        """Vacant Area - calculated as smu of premises leasable and dont occupied ares"""
        return sum(list(map(lambda p: p.area_size, self.premises.filter(Q(is_leasable=True) & Q(is_occupied=False)))))

    @property
    def nla(self):
        """Net Leased Area - amount of space under existing leases """
        return sum(list(map(lambda p: p.area_size, self.premises.filter(Q(is_leasable=True) & Q(is_occupied=True)))))

    @property
    def opex(self):
        """Operation Expenses Sum"""
        return sum(list(map(lambda o: o.monthly_value, self.opex_set.all())))

    @property
    def vacancy_rate(self):
        if self.gla:
            return self.vacant_area/self.gla
        else:
            return null

    @property
    def gross_rental_income(self):
        return sum(list(map(lambda r: r.rent, self.premises.rents.all())))

    @property
    def noi(self):
        """Net Operating Income - Effective_rental_income - operating_expenses"""
        return self.gross_rental_income - self.opex

    @property
    def market_value(self):
        """Direct Cap = Net_Cash_Flow / Capitalization_rate"""
        pass

    is_deleted = models.BooleanField(default=False)
    deleted = models.DateTimeField(blank=True, null=True)



    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

"""
class Floor(models.Model):
    label = models.CharField(max_length=250)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    description = models.TextField()
"""

class Premises(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True, related_name='premises')
    number = models.CharField(max_length=20)
    level = models.IntegerField(null=True, blank=True)
    is_leasable = models.BooleanField(null=True, blank=True)
    is_occupied = models.BooleanField(null=True, blank=True)
    area_size = models.FloatField(null=True, blank=True, default=0)
    area_unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name="+", null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = "Premises"
        verbose_name_plural = "Premises"

class OpexItem(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    default = models.BooleanField(default=False)
    owner =     owner = models.ForeignKey(
        'auth.User',
        related_name='opex_items',
        on_delete=models.PROTECT,
    )
    name = models.CharField(max_length=250)
    fullname = models.CharField(max_length=250, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Opex item"
        verbose_name_plural = "Opex items"

class CashFlowItem(models.Model):
    name = models.CharField(max_length=250)
    fullname = models.CharField(max_length=250)

class RentRoll(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    premises = models.ForeignKey(Premises, on_delete=models.CASCADE, related_name='rents')
    lease_start_date = models.DateField(null=True)
    lease_end_date = models.DateField(null=True)
    leased_area = models.FloatField(null=True)
    leased_area_unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name="+", null=True)
    rent = models.BigIntegerField(null=True)
    rent_currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="+", null=True)
    is_deleted = models.BooleanField(default=False)
    deleted = models.DateTimeField(blank=True, null=True)

class AssetOpex(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='opex_set')
    opex_item = models.ForeignKey(OpexItem, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_value = models.BigIntegerField()
    vat = models.IntegerField()
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="+")
    is_deleted = models.BooleanField(default=False)
    deleted = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Asset opex"
        verbose_name_plural = "Assets opexes"


