from typing import Any
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.views import View, generic
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from apps.accounts.models import PersonalProfile
from apps.business.models import Vacancy, Candidate
from .forms import PersonalInformationForm, PersonalProfileInformationForm, AcademicFormationForm
from .forms import ProfissionalFormationForm, ProfissionalExperienceForm, PersonalDocumentationForm
from .models import Formation, AcademicFormationItem, ProfissionalFormationItem
from .models import ProfissionalExperienceItem, ProfissionalExperience, Documentation

User = get_user_model()


class UserProfileView(View):
    template_name = "personal/user-profile.html"

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


user_profile = UserProfileView.as_view()


@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next"), ], name='dispatch')
class MyCandidateListView(View):
    """my candidate list view"""

    template_name = "personal/my-candidates.html"

    def get(self, request, *args, **kwargs):
        """get template list of vacancies applied"""
        candidates = Candidate.objects.filter(user=self.request.user)
        return render(self.request, self.template_name, {"candidates": candidates})


my_candidates = MyCandidateListView.as_view()


@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next"), ], name='dispatch')
class RegisterCandidacy(View):
    """ Register Candidacy View"""

    def post(self, request, *args, **kwargs):
        """ registers a candidate"""
        vacancy = Vacancy.objects.get(vid=self.kwargs.get('vid'))
        candidate = Candidate.objects.filter(user=self.request.user, vacancy=vacancy)

        if candidate.exists():
            messages.error(self.request, "You have already applied for this vacancy.")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER') or '')

        if self.request.user.type != "P":
            messages.error(self.request, "Only personal accounts can apply for vacancies.")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER') or '')

        documentations = Documentation.objects.filter(user=self.request.user)
        if not documentations.exists():
            messages.error(self.request,
                           "Your account does not have any documentation associated with the profile. Please complete your profile first!")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER') or '')

        documentation = documentations.first()
        if not documentation.cv:
            messages.error(self.request,
                           "Your account does not have a CV registered in the profile! Please add your CV first.")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER') or '')

        Candidate.objects.create(user=self.request.user, vacancy=vacancy, cv=documentation.cv)
        messages.success(self.request, "Your application has been submitted successfully!")
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER') or '')

apply_for_vacancy = RegisterCandidacy.as_view()


@method_decorator(
    [login_required(login_url='landing_page', redirect_field_name="next")], name='dispatch')
class VacancyDetailView(generic.DetailView):
    """Detail View for a specific vacancy"""
    model = Vacancy
    template_name = "personal/vacancy_detail.html"
    context_object_name = "vacancy"

    def get_object(self, *args, **kwargs):
        return Vacancy.objects.get(vid=self.kwargs.get('vid'))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx['applied'] = Candidate.objects.filter(
            user=self.request.user,
            vacancy=Vacancy.objects.get(vid=self.kwargs.get('vid'))
        ).exists()
        print(ctx)
        return ctx


vacancy_detail = VacancyDetailView.as_view()


@method_decorator([login_required(login_url='landing_page', redirect_field_name="next"), ], name='dispatch')
class VacancyListView(View):
    """render a list of vacancies for participants applying"""
    template_name = "personal/vacancy_list.html"

    def get(self, *args, **kwargs):
        """get template list of vacancies"""
        vacancies = Vacancy.objects.all()
        return render(self.request, self.template_name, {"vacancies": vacancies})


vacancy_list = VacancyListView.as_view()


@method_decorator([login_required(login_url='landing_page', redirect_field_name="next"), ], name='dispatch')
class CareerView(View):
    template_name = "personal/career.html"

    def get(self, request, *args, **kwargs):
        formation, _ = Formation.objects.get_or_create(user=request.user)
        experience, _ = ProfissionalExperience.objects.get_or_create(user=request.user)
        documentation, _ = Documentation.objects.get_or_create(user=request.user)

        personal_info_form = PersonalInformationForm(instance=request.user)
        personal_profile_form = PersonalProfileInformationForm(request.session.get('personal_info_form_data'),
                                                               instance=request.user.personal_profile)

        personal_academic_formation_form = AcademicFormationForm(
            request.session.get('personal_academic_formation_form_data', None))
        personal_profissional_formation_form = ProfissionalFormationForm(
            request.session.get('personal_profissional_formation_form_data', None))

        personal_profissional_experience_form = ProfissionalExperienceForm(
            request.session.get('personal_profissional_experience_form_data', None))
        personal_documentation_form = PersonalDocumentationForm(request.session.get('doc_files_form_data', None),
                                                                instance=documentation)

        acad_formation_items = AcademicFormationItem.objects.filter(formation=formation)
        prof_formation_items = ProfissionalFormationItem.objects.filter(formation=formation)

        prof_experience_items = ProfissionalExperienceItem.objects.filter(profissional_experience=experience)

        return render(self.request, self.template_name, {
            "personal_info_form": personal_info_form,
            "personal_profile_form": personal_profile_form,
            "personal_academic_formation_form": personal_academic_formation_form,
            "personal_profissional_formation_form": personal_profissional_formation_form,

            "personal_profissional_experience_form": personal_profissional_experience_form,
            "personal_documentation_form": personal_documentation_form,

            "acad_formation_items": acad_formation_items,
            "prof_formation_items": prof_formation_items,
            "prof_experience_items": prof_experience_items,

        })


career = CareerView.as_view()


@method_decorator([login_required(login_url='landing_page', redirect_field_name="next"), ], name='dispatch')
class AddDocumentation(View):
    form_class = PersonalDocumentationForm

    def post(self, request, *args, **kwargs):
        documentation, _ = Documentation.objects.get_or_create(user=request.user)
        request.session['personal_documentation_form_data'] = request.POST
        request.session['doc_files_form_data'] = request.FILES
        form = self.form_class(request.session['personal_documentation_form_data'], request.FILES,
                               instance=documentation)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.save()
            messages.success(request, "Documents uploaded successfully!")
            del (request.session['personal_documentation_form_data'])
            del (request.session['doc_files_form_data'])
        else:
            messages.error(request, "Error: Please upload all required documents!")
            print(form.errors)
        previous_page = self.request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_page or '')


add_documentation = AddDocumentation.as_view()


@method_decorator([login_required(login_url='landing_page', redirect_field_name="next"), ], name='dispatch')
class AddProfissionalExperienceItem(View):
    form_class = ProfissionalExperienceForm

    def post(self, request, *args, **kwargs):
        experience, created = ProfissionalExperience.objects.get_or_create(user=request.user)
        request.session['personal_profissional_experience_form_data'] = request.POST
        form = self.form_class(request.session['personal_profissional_experience_form_data'])
        if form.is_valid():
            experience_item = form.save(commit=False)
            experience_item.profissional_experience = experience
            experience_item.save()
            messages.success(request, "Professional experience added successfully!")
            del (request.session['personal_profissional_experience_form_data'])
        else:
            messages.error(request, "Error: Please fill out all fields!")
            print(form.errors)

        previous_page = self.request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_page or '')


add_profissional_experience = AddProfissionalExperienceItem.as_view()


@method_decorator([login_required(login_url='landing_page', redirect_field_name="next"), ], name='dispatch')
class DeleteProfissionalFormationItem(View):
    def post(self, *args, **kwargs):
        formation = ProfissionalFormationItem.objects.get(aid=self.kwargs['id'])
        formation.delete()
        messages.success(self.request, "Formation deleted successfully!")
        previous_page = self.request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_page or '')


delete_profissional_formation = DeleteProfissionalFormationItem.as_view()


@method_decorator([login_required(login_url='landing_page', redirect_field_name="next"), ], name='dispatch')
class DeleteAcademicFormationItem(View):
    def post(self, *args, **kwargs):
        formation = AcademicFormationItem.objects.get(aid=self.kwargs['id'])
        formation.delete()
        messages.success(self.request, "Formation deleted successfully!")
        previous_page = self.request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_page or '')


delete_academic_formation = DeleteAcademicFormationItem.as_view()


@method_decorator([login_required(login_url='landing_page', redirect_field_name="next"), ], name='dispatch')
class AddProfissionalFormationItem(View):
    form_class = ProfissionalFormationForm

    def post(self, request, *args, **kwargs):
        formation, created = Formation.objects.get_or_create(user=request.user)
        request.session['personal_profissional_formation_form_data'] = request.POST
        form = self.form_class(request.session['personal_profissional_formation_form_data'])
        if form.is_valid():
            formation_item = form.save(commit=False)
            formation_item.formation = formation
            formation_item.save()
            messages.success(request, "Professional formation added successfully!")
            del (request.session['personal_profissional_formation_form_data'])
        else:
            messages.error(request, "Error: Please fill in all fields!")
            print(form.errors)

        previous_page = self.request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_page or '')


add_profissional_formation = AddProfissionalFormationItem.as_view()


@method_decorator([login_required(login_url='landing_page', redirect_field_name="next"), ], name='dispatch')
class AddAcademicFormationItem(View):
    form_class = AcademicFormationForm

    def post(self, request, *args, **kwargs):
        formation, created = Formation.objects.get_or_create(user=request.user)

        request.session['personal_academic_formation_form_data'] = request.POST
        form = self.form_class(request.session['personal_academic_formation_form_data'])
        if form.is_valid():
            formation_item = form.save(commit=False)
            formation_item.formation = formation
            formation_item.save()
            messages.success(request, "Formation added successfully!")
            del (request.session['personal_academic_formation_form_data'])
        else:
            messages.error(request, "Error: Please fill in all fields!")
            print(form.errors)

        previous_page = self.request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_page or '')


add_academic_formation = AddAcademicFormationItem.as_view()


@method_decorator([login_required(login_url='landing_page', redirect_field_name="next"), ], name='dispatch')
class ProfileUpdateView(View):
    form_class = PersonalProfileInformationForm

    def post(self, request, *args, **kwargs):
        profile = request.user.personal_profile
        request.session['personal_info_form_data'] = request.POST
        form = self.form_class(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            # user_profile.save()
            messages.success(request, "Profile updated successfully!")
            del (request.session['personal_info_form_data'])
        else:
            messages.error(request, "Error: Please fill in all fields!")
            print(form.errors)
        previous_page = self.request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(previous_page or '')


profile_update = ProfileUpdateView.as_view()