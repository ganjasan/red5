from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Asset)
admin.site.register(Currency)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Region)
admin.site.register(Microlocation)
admin.site.register(Unit)
admin.site.register(Property)
admin.site.register(Premises)
admin.site.register(OpexItem)
admin.site.register(CashFlowItem)
admin.site.register(RentRoll)
admin.site.register(AssetOpex)