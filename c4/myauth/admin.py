from django.contrib import admin
from .models import Profile,OTPRequest

class ProfileAdmin(admin.ModelAdmin):
    list_display = ( 'get_username', 'get_first_name', 'get_last_name','phone_number')
    search_fields = ['user__username', 'phone_number']

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'Username'

    def get_first_name(self, obj):
        return obj.user.first_name

    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name

    get_last_name.short_description = 'Last Name'

    fieldsets = (
        ('User Details', {
            'fields': ('user',)
        }),
        ('Profile Information', {
            'fields': ('phone_number',)
        }),
    )

    readonly_fields = ('get_username', 'get_first_name', 'get_last_name')


admin.site.register(Profile,ProfileAdmin)
