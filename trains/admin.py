from django.contrib import admin
from trains.models import Train

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ['title', 'capacity', 'city_from', 'city_to', 'created_at']
