""" admin config for vacancy in the django admin dashboard"""
from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import JobType, Benefit, Candidate
from .models import Vacancy, Responsibility, Skill

User = get_user_model()


@admin.register(Candidate)
class CandidatesAdmin(admin.ModelAdmin):
    """register candidates in the django admin dashboard"""
    list_display = ['user', 'vacancy', 'cv', 'created_at']
    list_display_links = ['user', 'vacancy', 'cv', 'created_at']
    search_fields = ['user', 'vacancy', 'cv', 'created_at']
    list_per_page = 20


class BenefitAdminInline(admin.TabularInline):
    """job benefits tabular mode for admin panel"""
    model = Benefit
    extra = 0


class ResponsibilityAdminInline(admin.TabularInline):
    """job responsibility tabular mode for admin panel"""
    model = Responsibility
    extra = 0


class SkillAdminInline(admin.TabularInline):
    """job skill tabular mode for admin panel"""
    model = Skill
    extra = 0


@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    """job type class for putting in admin panel"""
    list_display = ['id', 'title', 'created_at']
    list_display_links = ['id', 'title', 'created_at']
    search_fields = ['title', 'created_at']
    list_per_page = 20


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    """vacancy class for putting in admin panel"""
    list_display = ['id', 'title', 'company', 'min_wage', 'max_wage', 'created_at']
    list_display_links = ['id', 'title', 'company', 'min_wage', 'max_wage', 'created_at']
    search_fields = ['title', 'company', 'min_wage', 'max_wage']
    list_filter = ['title', 'company', 'min_wage', 'max_wage', 'description']
    list_per_page = 20
    inlines = [SkillAdminInline, ResponsibilityAdminInline, BenefitAdminInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set the company if the vacancy is being created
            obj.company = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(company=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "company":
            kwargs["queryset"] = User.objects.filter(pk=request.user.pk)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
