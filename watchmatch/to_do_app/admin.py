from django.contrib import admin
from to_do_app.models import Movie,StreamPlatform,WatchList,Review,User
# Register your models here.
admin.site.register([User,Movie,StreamPlatform,WatchList,Review])

