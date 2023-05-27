from django.contrib import admin
from django.contrib.auth.models import User

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
    list_filter = ('isConverted',)
    search_fields = ['company_name']
    sortable_field_name = ['company_name',
                           'isConverted',
                           'date_created',
                           'date_updated',
                           'isConverted',
                           'sales_contact'
                           ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name="Managermen").exists():
            return qs
        return qs.filter(sales_contact=request.user)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "sales_contact":
            kwargs["queryset"] = User.objects.filter(groups__name='Salesmen')
        return super(ClientAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class ContractAdmin(admin.ModelAdmin):
    readonly_fields = ('client',)
    list_display = ('id',
                    'status',
                    'amount',
                    'payment_due',
                    'date_created',
                    'date_updated',
                    'client',
                    'sales_contact'
                    )
    list_filter = ('status', 'payment_due')
    search_fields = ['status', 'client']
    sortable_field_name = ['status',
                           'amount',
                           'payment_due',
                           'date_created',
                           'date_updated',
                           'client',
                           'sales_contact'
                           ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name="Managermen").exists():
            return qs
        return qs.filter(sales_contact=request.user)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "sales_contact":
            kwargs["queryset"] = User.objects.filter(groups__name='Salesmen')
        return super(ContractAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)



class EventAdmin(admin.ModelAdmin):
    readonly_fields = ('client', 'contract')
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
    list_filter = ('status', 'date_event')
    search_fields = ['client']
    sortable_field_name = ['attendees',
                           'date_event',
                           'status',
                           'date_created',
                           'date_updated',
                           'client',
                           'support_contact'
                           ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name="Managermen").exists():
            return qs
        return qs.filter(support_contact=request.user)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "support_contact":
            kwargs["queryset"] = User.objects.filter(groups__name='Supportmen')
        return super(EventAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)
