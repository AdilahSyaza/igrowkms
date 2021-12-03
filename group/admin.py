from django.contrib import admin
from .models import Group, GroupMembership, GroupSoilTag, GroupPlantTag

# Register your models here.

admin.site.register(Group)
admin.site.register(GroupMembership)
admin.site.register(GroupSoilTag)
admin.site.register(GroupPlantTag)
