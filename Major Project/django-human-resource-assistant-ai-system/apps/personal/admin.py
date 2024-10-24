from django.contrib import admin
from .models import *

class ProfissionalExperienceItemAdminInline(admin.TabularInline):
   model = ProfissionalExperienceItem
   extra = 0



@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
   list_display = ['id', 'user', 'bi', 'cv', 'certificate_literary','created_at']
   list_display_links = ['id', 'user', 'bi', 'cv', 'certificate_literary', 'created_at']
   search_fields = ['user', 'bi', 'cv', 'certificate_literary']
   list_per_page = 10


@admin.register(ProfissionalExperience)
class ProfissionalExperienceAdmin(admin.ModelAdmin):
   list_display = ['id', 'user', 'created_at']
   list_display_links = ['id', 'user', 'created_at']
   list_per_page = 20
   inlines = [ProfissionalExperienceItemAdminInline]


@admin.register(AcademicInstitution)
class AcademicInstituitionAdmin(admin.ModelAdmin):
   list_display = ['id', 'name', 'created_at']
   list_display_links = ['id', 'name', 'created_at']
   list_per_page = 20

@admin.register(ProfissionalInstitution)
class ProfissionalInstituitionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    list_display_links = ['id', 'name', 'created_at']
    list_per_page = 20

class AcademicFormationItemAdminInline(admin.TabularInline):
   model = AcademicFormationItem
   extra = 0

class ProfissionalFormationItemAdminInline(admin.TabularInline):
   model = ProfissionalFormationItem
   extra = 0

@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at',)
    list_display_links = ('id','user', 'created_at',)
    list_per_page = 20
    inlines = [AcademicFormationItemAdminInline, ProfissionalFormationItemAdminInline]