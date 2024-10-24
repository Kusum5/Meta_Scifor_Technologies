from django.urls import reverse
from django.http import HttpResponse
from django.views import View, generic
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class LandingPageView(generic.View):
    template_name = 'landing-page.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('accounts:controller'))
        return render(self.request, self.template_name, {})
         
landing_page_view = LandingPageView.as_view()
    