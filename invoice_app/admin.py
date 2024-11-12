from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _

# Register your models here.
class AdminCustomer(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'sex', 'age', 'city', 'zip_code')

class AdminInvoice(admin.ModelAdmin):
    list_display = ('customer', 'save_by', 'invoice_date', 'total', 'last_updated_time', 'paid', 'invoice_type')

class AdminArticle(admin.ModelAdmin):
    list_display = ('invoice', 'name', 'quantity', 'unit_price', 'total')

admin.site.register(Customer, AdminCustomer)
admin.site.register(Invoice, AdminInvoice)
admin.site.register(Article, AdminArticle)

admin.site.index_title = _('FAEK CORP')
admin.site.site_header = _('FAEK CORP')
admin.site.index_title = _('FAEK CORP')
