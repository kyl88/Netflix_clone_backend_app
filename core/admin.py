from django.contrib import admin

# import from models

from .models import Movie

# Register your models here.

admin.site.register(Movie)