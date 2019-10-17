from django.contrib import admin
from .models import *

# Register your models here.
models = [User, Favorite]
admin.site.register(models)
