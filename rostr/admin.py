from django.contrib.sessions.models import Session
from django.contrib import admin

from models import Roster, Store


class RosterAdmin(admin.ModelAdmin):
    list_display = ('event_title',  'event_location', 'success', 'downloaded', 'created', 'method')
    list_display_links = ('event_title',  'event_location')
    search_fields = ['event_title', 'event_location']
    list_filter = ('method', 'created', 'success', 'downloaded', 'error')
    ordering = ('-created',)
    readonly_fields = ('created', 'dump', 'success', 'downloaded', 'token', 'method')
    actions = ['clean_deferred_data', 'resolve_errors']

    fieldsets = (
        ('Roster information', {
            'fields': (
                'event_title',
                ('event_location', 'store'),
                'hours',
                'saturday'
            )
        }),
        ('Meta', {
            'fields': (
                ('success', 'downloaded'),
                'token',
                'method',
                'created',
                'error',
                'dump',
                'raw_roster'
            )
        }),
    )

    def clean_deferred_data(self, request, queryset):
        rows_updated = queryset.update(dump=None)
        if rows_updated == 1:
            message_bit = "1 roster"
        else:
            message_bit = "%s rosters" % rows_updated
        self.message_user(request, "Successfully removed deferred data from %s" % message_bit)
    clean_deferred_data.short_description = "Clean deferred data"

    def resolve_errors(self, request, queryset):
        rows_updated = queryset.update(error='_resolved_')
        if rows_updated == 1:
            message_bit = "1 roster"
        else:
            message_bit = "%s rosters" % rows_updated
        self.message_user(request, "Successfully resolve errors for %s" % message_bit)
    resolve_errors.short_description = "Mark errors as resolved"


class StoreAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'name', 'number', 'address', 'country',)
    list_filter = ('country',)
    list_display_links = ('image_tag', 'name')
    search_fields = ('name', 'number', 'address', 'country')
    fieldsets = (
        ('Store Information', {
            'fields': (
                ('name'),
                ('address', 'country'),
                'phone',
                ('number', 'retailme_id'),
                ('link', 'image'),
                ('geoposition'),
            )
        }),
    )

admin.site.register(Roster, RosterAdmin)
admin.site.register(Store, StoreAdmin)


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']

admin.site.register(Session, SessionAdmin)
