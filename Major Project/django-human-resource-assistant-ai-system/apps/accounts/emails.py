from django.conf import settings
from django.shortcuts import render
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_register_welcome(user, email:str,project_name:str, company_address:str,
                          action_url:str, support_email:str ="", login_url:str ="", 
                          project_website:str =""):
    subject = 'Bem-vindo(a) a EJZ Tecnologia'
    list_emails = [email,]

    html_content = render_to_string('emails/accounts/register-welcome.html', {"user":user, 
                                                                   "project_name":project_name, 
                                                                   "company_address":company_address, 
                                                                   "action_url":action_url})
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=settings.EMAIL_HOST_USER,to=list_emails)
    email.attach_alternative(html_content, 'text/html')
    email.send()

def send_password_reset(user, email:str,project_name:str, company_address:str,action_url:str):
    subject = 'Definir Palavra-passe na EJZ Tecnologia'
    list_emails = [email,]

    html_content = render_to_string('emails/accounts/password-reset.html', {"user":user, 
                                                                   "project_name":project_name, 
                                                                   "company_address":company_address, 
                                                                   "action_url":action_url})
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=settings.EMAIL_HOST_USER,to=list_emails)
    email.attach_alternative(html_content, 'text/html')
    email.send()
