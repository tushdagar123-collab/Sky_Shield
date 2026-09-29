from django.contrib import admin
from .models import Incident


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'severity',
        'status',
        'aircraft_type',
        'location',
        'date_time',
        'reported_by',
        'created_at',
    )
    list_filter = ('category', 'severity', 'status', 'created_at', 'date_time')
    search_fields = ('title', 'description', 'location', 'aircraft_type', 'reported_by__username')
    date_hierarchy = 'date_time'
    ordering = ('-date_time',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'date_time', 'location')
        }),
        ('Classification & Aircraft', {
            'fields': ('aircraft_type', 'category', 'severity', 'status')
        }),
        ('Reporting Metadata', {
            'fields': ('reported_by', 'created_at')
        }),
    )
