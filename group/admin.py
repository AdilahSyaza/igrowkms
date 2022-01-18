from django.contrib import admin
from .models import Group_tbl, GroupMembership, GroupSoilTagging, GroupPlantTagging

# Register your models here.

admin.site.register(Group_tbl)
admin.site.register(GroupMembership)
# admin.site.register(GroupSoilTag)
# admin.site.register(GroupPlantTag)
admin.site.register(GroupSoilTagging)
admin.site.register(GroupPlantTagging)
