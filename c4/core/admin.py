from django.contrib import admin
from .models import Project,Participation,C4Group

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'units_number', 'project_area', 'completed_units_number', 'contractor_name')
    search_fields = ['title', 'contractor_name']
    list_filter = ['status']
    list_editable = ['status']

    fieldsets = (
        ('Project Details', {
            'fields': ('title', 'status', 'units_number', 'project_area', 'completed_units_number', 'contractor_name')
        }),
        ('Location', {
            'fields': ('location_x', 'location_y')
        }),
        ('Additional Information', {
            'fields': ('units_facilities')
        }),
    )

class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'project', 'unit', 'payment_valid')
    search_fields = ['profile__user__username', 'project__title']
    list_filter = ['payment_valid']
    list_editable = ['payment_valid']

    fieldsets = (
        ('Participant Details', {
            'fields': ('profile', 'project', 'unit')
        }),
        ('Payment Information', {
            'fields': ('receipt_photo', 'payment_valid')
        }),
    )

class C4GroupAdmin(admin.ModelAdmin):
    list_display = ('project', 'creator', 'status', 'unit')
    search_fields = ['project__title', 'creator__user__username']
    list_filter = ['status']
    list_editable = ['status']

    fieldsets = (
        ('Group Details', {
            'fields': ('project', 'creator', 'unit')
        }),
        ('Core Members', {
            'fields': ('core1', 'core2', 'core3')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )

admin.site.register(Project,ProjectAdmin)
admin.site.register(Participation,ParticipationAdmin)
admin.site.register(C4Group,C4GroupAdmin)
