import calendar
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.contrib.auth import get_user_model

from apps.accounts.models import PersonalProfile
from apps.personal.models import Documentation
from apps.accounts.utils import GENDER
from .models import Vacancy
User = get_user_model()


def get_users_without_cv_pie():
    # Contar quantos usuários têm CV e quantos não têm
    with_cv = Documentation.objects.filter(cv__isnull=False).count()
    without_cv = Documentation.objects.filter(cv__isnull=True).count()

    # Preparar os dados para o Chart.js
    labels = ['Com CV', 'Sem CV']
    data = [with_cv, without_cv]

    return (labels, data,)

def get_users_gender_pie():
    gender_data = PersonalProfile.objects.values('gender').annotate(total=Count('gender'))
    # Preparar os dados para o Chart.js
    labels = [dict(GENDER)[item['gender']] for item in gender_data]
    data = [item['total'] for item in gender_data]
    return (labels, data,)

def get_users_by_month():
    users = User.objects.annotate(month=TruncMonth('date_joined')).values('month').annotate(total=Count('id')).order_by('month')
    labels = []
    data = []
    for user in users:
        month_name = calendar.month_name[user['month'].month]
        labels.append(month_name)
        data.append(user['total'])
    return (labels, data,)

def get_vacancies_by_month():
    vacancies = Vacancy.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(total=Count('id')).order_by('month')
    labels = []
    data = []
    for vacancy in vacancies:
        month_name = calendar.month_name[vacancy['month'].month]
        labels.append(month_name)
        data.append(vacancy['total'])
    return (labels, data,)

