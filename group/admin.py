from django.contrib import admin
from .models import Group, GroupMembership, GroupSoilTagging, GroupPlantTagging

# Register your models here.

admin.site.register(Group)
admin.site.register(GroupMembership)
# admin.site.register(GroupSoilTag)
# admin.site.register(GroupPlantTag)
admin.site.register(GroupSoilTagging)
admin.site.register(GroupPlantTagging)
