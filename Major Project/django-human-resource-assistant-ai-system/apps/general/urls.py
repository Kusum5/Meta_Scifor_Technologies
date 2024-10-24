from . import views 
from django.urls import path

urlpatterns = [
    path('', views.LandingPageView.as_view(),name="landing_page"),
    # path('search/', views.search, name='search'),
    # path('', views.home,name="home"),

    # path('get_notifications/<int:id>', views.get_notifications, name='get-notifications'),
    # path('read-all-notifications/', views.read_all_notifications, name='read-all-notifications'),
    # path('read-notification-material-requisition/<int:id>', views.read_notification, name='read-notification'),
    # path('solicitations/send/<int:id>', views.send_notification_material_req, name="send-notification-material-req"),
]
