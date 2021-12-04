from django.contrib import admin
from .models import Person
from .models import Room
from .models import Message
from .models import MemberRequest
from .models import Memberlist
from .models import SensorData
# from .models import Plants
from .models import SoilTag
from .models import PlantTag
# from .models import Comment
from .models import *

admin.site.register(Person)
admin.site.register(Room)
admin.site.register(Message)

admin.site.register(MemberRequest)
admin.site.register(Memberlist)
admin.site.register(SensorData)
# admin.site.register(Plants)

admin.site.register(SoilTag)
admin.site.register(PlantTag)

# Register your models here.
admin.site.register(Users)
