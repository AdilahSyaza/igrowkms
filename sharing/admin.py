from django.contrib import admin
from .models import Comment
from .models import Feed
from .models import FeedSoilTagging

admin.site.register(Comment)
admin.site.register(Feed)
admin.site.register(FeedSoilTagging)

# Register your models here.
