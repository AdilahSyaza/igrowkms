from django.contrib import admin
from .models import Booking
from .models import Workshop
from .models import SoilTag

# Register your models here.

admin.site.register(Booking)
admin.site.register(Workshop)
admin.site.register(SoilTag)