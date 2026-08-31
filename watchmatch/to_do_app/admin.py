from django.contrib import admin
from to_do_app.models import Movie,StreamPlatform,WatchList,Review
# Register your models here.
admin.site.register([Movie,StreamPlatform,WatchList,Review])

