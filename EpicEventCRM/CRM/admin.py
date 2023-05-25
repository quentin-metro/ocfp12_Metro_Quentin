from django.contrib import admin
from .models import Client, Contract, Event


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'company_name',
                    'email',
                    'phone',
                    'mobile',
                    'first_name',
                    'last_name',
                    'date_created',
                    'date_updated',
                    'isConverted',
                    'sales_contact'
                    )


class ContractAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'status',
                    'amount',
                    'payment_due',
                    'date_created',
                    'date_updated',
                    'client',
                    'sales_contact'
                    )


class EventAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'attendees',
                    'date_event',
                    'notes',
                    'status',
                    'date_created',
                    'date_updated',
                    'client',
                    'support_contact'
                    )



admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)
