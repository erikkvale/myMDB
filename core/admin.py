from django.contrib import admin
from core.models import (
    Movie
)

# Register your models here.
admin.site.register(Movie)
admin.site.site_header = 'myMDB Admin'
admin.site.site_title = 'myMDB Admin Portal'
admin.site.index_title = 'Welcome to the myMDB Admin Portal'