""" Business Views"""
from django.db.models import Count
from django.views import View
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import get_user_model

from apps.personal.models import Formation, ProfissionalExperience, Documentation
from apps.personal.models import AcademicFormationItem, ProfissionalFormationItem
from apps.personal.models import ProfissionalExperienceItem

from apps.business.models import Skill, Responsibility, Benefit
from .models import Vacancy, Candidate
from .forms import RegisterVacancyForm, VacancySkillForm
from .forms import VacancyResponsibilityForm, VacancyBenefitForm
from . import charts

User = get_user_model()


class CandidateUserProfileView(View):
    template_name = "business/candidate-user-profile.html"

    def get(self, request, *args, **kwargs):
        owner = User.objects.get(uid=self.kwargs.get('uid'))
        formation, _ = Formation.objects.get_or_create(user=owner)
        experience, _ = ProfissionalExperience.objects.get_or_create(user=owner)
        documentation, _ = Documentation.objects.get_or_create(user=owner)

        acad_formation_items = AcademicFormationItem.objects.filter(formation=formation)
        prof_formation_items = ProfissionalFormationItem.objects.filter(formation=formation)
        prof_experience_items = ProfissionalExperienceItem.objects.filter(profissional_experience=experience)

        candidates = Candidate.objects.filter(user=owner)

        return render(self.request, self.template_name, {
            "acad_formation_items": acad_formation_items,
            "prof_formation_items": prof_formation_items,
            "prof_experience_items": prof_experience_items,
            "documentation": documentation,
            "candidates": candidates,
            "owner": owner,
        })


candidate_user_profile = CandidateUserProfileView.as_view()


def user_profile(request, uid):
    total_vacancies = Vacancy.objects.filter(company=request.user)
    total_vacancies_active = Vacancy.objects.filter(company=request.user, expiration_data__gt=timezone.now().date())
    total_users = User.objects.exclude(uid=request.user.uid)
    total_candidates = Candidate.objects.all()
    labels_bar_vacancies_by_month, data_bar_vacancies_by_month = charts.get_vacancies_by_month()
    labels_users_by_month_line, data_users_by_month_line = charts.get_users_by_month()
    labels_users_gender_pie, data_users_gender_pie = charts.get_users_gender_pie()
    labels_users_without_pie, data_users_without_pie = charts.get_users_without_cv_pie()

    print(labels_users_by_month_line)
    print(data_users_by_month_line)

    return render(request, "business/user-profile.html", {
        'total_vacancies': total_vacancies,
        'total_vacancies_active': total_vacancies_active,
        'total_users': total_users,
        'total_candidates': total_candidates,
        'labels_bar_vacancies_by_month': labels_bar_vacancies_by_month,
        'data_bar_vacancies_by_month': data_bar_vacancies_by_month,
        'labels_users_by_month_line': labels_users_by_month_line,
        'data_users_by_month_line': data_users_by_month_line,
        'labels_users_gender_pie': labels_users_gender_pie,
        'data_users_gender_pie': data_users_gender_pie,
        'labels_users_without_pie': labels_users_without_pie,
        'data_users_without_pie': data_users_without_pie,
    })


@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")], name='dispatch')
class CandidacyAnalysesView(View):
    """analyses View """
    model = Candidate
    template_name = "business/candidacy_analyses.html"
    context_object_name = 'candidates'

    def get(self, request, *args, **kwargs):
        """get all  candidates applied to the vacancy"""
        vacancy = Vacancy.objects.get(vid=self.kwargs.get('vid'))
        candidates = Candidate.objects.filter(vacancy=vacancy)
        total_candidates = len(candidates)
        # paginator = Paginator(list_candidates,5)
        # candidates = paginator.get_page(self.request.GET.get('page'))

        return render(self.request, self.template_name,
                      {'candidates': candidates, "vacancy": vacancy,
                       "total_candidates": total_candidates})


candidacy_analyses = CandidacyAnalysesView.as_view()


@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")], name='dispatch')
class CandidacyListView(View):
    """List View for all candidate applied in a vacancy"""
    model = Candidate
    template_name = "business/candidacy_list.html"
    context_object_name = 'candidates'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        """get all  candidates applied to the vacancy"""
        vacancy = Vacancy.objects.get(vid=self.kwargs.get('vid'))
        list_candidates = Candidate.objects.filter(vacancy=vacancy)
        total_candidates = len(list_candidates)
        paginator = Paginator(list_candidates, 5)
        candidates = paginator.get_page(self.request.GET.get('page'))

        return render(self.request, self.template_name,
                      {'candidates': candidates, "vacancy": vacancy, "total_candidates": total_candidates})


candidacy_list = CandidacyListView.as_view()


class _BasicVacancyEditViewModel(View):
    template_name = "business/vacancy_edit.html"
    form_class = RegisterVacancyForm

    def get_instance(self) -> Vacancy:
        """get the current edit instance of vacancy 
        Returns:
            Vacancy: current vacancy
        """
        vacancy = Vacancy.objects.get(vid=self.kwargs.get("vid"))
        return vacancy

    def get(self, *args, **kwargs):
        """retrieve edit page with forms"""
        vacancy = self.get_instance()
        vacancy_information_form = self.form_class(self.request.session.get("vacancy_basic_form_data", None),
                                                   instance=vacancy)
        vacancy_skills_form = VacancySkillForm(self.request.session.get("vacancy_skills_form_data", None))
        vacancy_responsibilities_form = VacancySkillForm(
            self.request.session.get("vacancy_responsibility_form_data", None))
        vacancy_benefits_form = VacancySkillForm(self.request.session.get("vacancy_benefits_form_data", None))
        return render(self.request, self.template_name, {
            "vacancy": vacancy,
            "vacancy_information_form": vacancy_information_form,
            "vacancy_skills_form": vacancy_skills_form,
            "vacancy_responsibilities_form": vacancy_responsibilities_form,
            "vacancy_benefits_form": vacancy_benefits_form
        })


@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")], name='dispatch')
class VacancyBenefitsViewEdit(_BasicVacancyEditViewModel):
    """edit vacancy skills view"""
    form_class = VacancyBenefitForm

    def post(self, *args, **kwargs):
        """ save benefits"""
        self.request.session['vacancy_benefits_form_data'] = self.request.POST
        form = self.form_class(self.request.POST)
        if form.is_valid():
            benefit = form.save(commit=False)
            benefit.vacancy = self.get_instance()
            benefit.save()
            messages.success(self.request, "Benefit saved successfully!")
            del self.request.session['vacancy_benefits_form_data']
        print(form.errors)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER') or '')


add_vacancy_benefits = VacancyBenefitsViewEdit.as_view()


@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")], name='dispatch')
class VacancyResponsibilityViewEdit(_BasicVacancyEditViewModel):
    """edit vacancy responsibility view"""
    form_class = VacancyResponsibilityForm

    def post(self, *args, **kwargs):
        """ save responsibility"""
        self.request.session['vacancy_responsibility_form_data'] = self.request.POST
        form = self.form_class(self.request.POST)
        if form.is_valid():
            responsibility = form.save(commit=False)
            responsibility.vacancy = self.get_instance()
            responsibility.save()
            messages.success(self.request, "Responsibility saved successfully!")
            del self.request.session['vacancy_responsibility_form_data']
        print(form.errors)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER') or '')


add_vacancy_responsibilities = VacancyResponsibilityViewEdit.as_view()


@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")], name='dispatch')
class VacancySkillSViewEdit(_BasicVacancyEditViewModel):
    """edit vacancy skills view"""
    form_class = VacancySkillForm

    def post(self, *args, **kwargs):
        """ save skills"""
        self.request.session['vacancy_skills_form_data'] = self.request.POST
        form = self.form_class(self.request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.vacancy = self.get_instance()
            skill.save()
            messages.success(self.request, "Requirement saved successfully!")
            del self.request.session['vacancy_skills_form_data']
        print(form.errors)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER') or '')


add_vacancy_skills = VacancySkillSViewEdit.as_view()


@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")], name='dispatch')
class DeleteResponsibilityView(View):
    """delete vacancy responsibility view"""

    def post(self, *args, **kwargs):
        """post method for delete processing request
        Returns:
            http redirect response: redirect url view
        """
        responsibility = Responsibility.objects.get(rid=self.kwargs.get('rid'))
        responsibility.delete()
        messages.success(self.request, "Responsibility deleted successfully!")
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER') or '')


delete_responsibility = DeleteResponsibilityView.as_view()


@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")], name='dispatch')
class DeleteBenefitView(View):
    """delete vacancy benefit view"""

    def post(self, *args, **kwargs):
        """post method for delete processing request
        Returns:
            http redirect response: redirect url view
        """
        benefit = Benefit.objects.get(bid=self.kwargs.get('bid'))
        benefit.delete()
        messages.success(self.request, "Benefit deleted successfully!")
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER') or '')


delete_benefit = DeleteBenefitView.as_view()


@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")], name='dispatch')
class DeleteSkillView(View):
    """delete vacancy skill view"""

    def post(self, *args, **kwargs):
        """post method for delete processing request
        Returns:
            http redirect response: redirect url view
        """
        skill = Skill.objects.get(sid=self.kwargs.get('sid'))
        skill.delete()
        messages.success(self.request, "Requirement deleted successfully!")
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER') or '')


delete_skill = DeleteSkillView.as_view()


@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next"), ], name='dispatch')
class EditVacancyView(_BasicVacancyEditViewModel):
    """edit vacancy view"""

    def post(self, request, *args, **kwargs):
        """ save vacancy edit"""
        request.session['vacancy_basic_form_data'] = request.POST
        form = self.form_class(request.POST, instance=self.get_instance())
        if form.is_valid():
            form.save()
            messages.success(request, "Vacancy edited successfully!")
            del request.session['vacancy_basic_form_data']
        print(form.errors)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER') or '')


edit_vacancy = EditVacancyView.as_view()


@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")], name='dispatch')
class DeleteVacancyView(View):
    """delete vacancy view"""

    def post(self, *args, **kwargs):
        """post method for delete processing request
        Returns:
            http redirect response: redirect url view
        """
        vacancy = Vacancy.objects.get(vid=self.kwargs.get('vid'))
        vacancy.delete()
        messages.success(self.request, "Vacancy deleted successfully!")
        return redirect(reverse('business:vacancy-list'))


delete_vacancy = DeleteVacancyView.as_view()


@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")], name='dispatch')
class VacancyDetailView(generic.DetailView):
    """Detail View for a specific vacancy"""
    model = Vacancy
    template_name = "business/vacancy_detail.html"
    context_object_name = "vacancy"

    def get_object(self, *args, **kwargs):
        return Vacancy.objects.get(vid=self.kwargs.get('vid'))


vacancy_detail = VacancyDetailView.as_view()


@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")], name='dispatch')
class VacancyListView(generic.ListView):
    """List View for all vacancies"""
    model = Vacancy
    template_name = "business/vacancy_list.html"
    context_object_name = 'vacancies'

    def get_queryset(self):
        """get all my published vacancies annotated with the number of candidates"""
        return Vacancy.objects.filter(is_published=True, company=self.request.user).annotate(
            candidate_count=Count('candidate')
        )


vacancy_list = VacancyListView.as_view()


@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")], name='dispatch')
class RegisterVacancyView(View):
    """ Register Vacancy View"""
    template_name = 'business/register_vacancy.html'
    form_class = RegisterVacancyForm

    def get(self, request):
        """register get method to retrieve form"""
        register_vacancy_form = self.form_class(request.session.get("register_vacancy_form_data"))
        return render(request, self.template_name, {"register_vacancy_form": register_vacancy_form})

    def post(self, request):
        """Register post method to save form data"""
        self.request.session["register_vacancy_form_data"] = self.request.POST
        form = self.form_class(self.request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.company = self.request.user
            vacancy.save()
            del request.session['register_vacancy_form_data']
            messages.success(self.request, "Vacancy registered successfully!")
            return redirect(reverse('business:vacancy-list'))
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER') or '')

register_vacancy = RegisterVacancyView.as_view()