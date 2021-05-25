from django.contrib import admin
# from .models import related models
from . import models


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = models.CarModel 
    extra = 5

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

# Register models here
admin.site.register(models.CarMake, CarMakeAdmin)
admin.site.register(models.CarModel)