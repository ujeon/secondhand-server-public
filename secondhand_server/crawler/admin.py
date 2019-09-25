from django.contrib import admin
from .models import *

# Register your models here.
models = [Raw_data, Category, Filtered_data, Average_price]
admin.site.register(models)

