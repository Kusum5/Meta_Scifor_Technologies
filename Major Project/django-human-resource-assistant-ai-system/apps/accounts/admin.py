from django.contrib import admin
from .models import PersonalProfile, CompanyProfile, Sector
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'username', 'email', ]
    list_display_links = ['id', 'first_name', 'last_name', 'username', 'email', ]
    search_fields = ['first_name', 'last_name', 'username', 'email']
    list_per_page = 20


admin.site.register(User, UserAdmin)


class SectorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', ]
    list_display_links = ['id', 'name', 'created_at', ]
    list_per_page = 25
    list_filter = ['name', 'created_at']


admin.site.register(Sector, SectorAdmin)


class PersonalProfileAdmin(admin.ModelAdmin):
    list_display = ['get_user']
    list_display_links = ['get_user', ]
    list_per_page = 25

    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    get_user.short_description = 'Nome do Usuario'


admin.site.register(PersonalProfile, PersonalProfileAdmin)


class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['get_user']
    list_display_links = ['get_user', ]
    list_per_page = 25

    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    get_user.short_description = 'Nome do Usuario'


admin.site.register(CompanyProfile, CompanyProfileAdmin)
