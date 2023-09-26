from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('car_make', 'name', 'dealer_id', 'type', 'year')
    list_filter = ['car_make__name', 'name', 'dealer_id', 'type', 'year']
    search_fields = ['car_make__name', 'name']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name', 'description')
    list_filter = ['name']
    search_fields = ['name']

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
