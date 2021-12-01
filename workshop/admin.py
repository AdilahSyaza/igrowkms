from django.contrib import admin
from .models import Booking
from .models import Workshop
from .models import SoilTag
from .models import PlantTag

# Register your models here.

admin.site.register(Booking)
admin.site.register(Workshop)
admin.site.register(SoilTag)
admin.site.register(PlantTag)