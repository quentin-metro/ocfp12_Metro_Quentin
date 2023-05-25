"""
URL configuration for EpicEventCRM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from CRM.views import login_redirect
from CRM.views import client_get_list, client_create, client_handler, client_convert, client_get_contract_or_sign
from CRM.views import contract_get_list, contract_handler, contract_event, contract_client
from CRM.views import event_get_list, event_handler, event_end, event_client

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('redirect/', login_redirect, name='login_redirect'),
    path('admin/', admin.site.urls, name='admin'),
    path('clients/', client_get_list, name='clients'),
    path('clients/new', client_create, name='new_client'),
    path('clients/<int:client_id>/', client_handler, name='client_handler'),
    path('clients/<int:client_id>/convert', client_convert, name='convert_client'),
    path('clients/<int:client_id>/contract/', client_get_contract_or_sign, name='client_contract'),
    path('contracts/', contract_get_list, name='contracts'),
    path('contracts/<int:contract_id>', contract_handler, name='contract_handler'),
    path('contracts/<int:contract_id>/event', contract_event, name='contract_event'),
    path('contracts/<int:contract_id>/client', contract_client, name='event_client'),
    path('events/', event_get_list, name='events'),
    path('events/<int:event_id>/', event_handler, name='events_handler'),
    path('events/<int:event_id>/end', event_end, name='events_end'),
    path('events/<int:event_id>/client', event_client, name='events_client'),
]
