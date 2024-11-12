from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from django.conf import settings
from .models import *
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
import pdfkit
from django.template.loader import get_template
import datetime
from .utils import pagination, seeInvoice
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
import qrcode
from io import BytesIO
import base64
from .decorators import * 
from django.utils.translation import gettext as _

# Create your views here.
class HomeView(LoginRequiredSuperuserMixin, View):
    """ Main/Home view """

    template_name = 'index.html'

    invoices = Invoice.objects.select_related('customer', 'save_by').all().order_by('-invoice_date') 

    context = {
            'invoices': invoices,
            'languages': settings.LANGUAGES
        }

    def get(self, request, *args, **kwargs):

        items = pagination(request, self.invoices)
        self.context['invoices'] = items

        return render(request, self.template_name, self.context) 


    def post(self, request, *args, **kwargs):

    # Logic For Marking the invoice as Paid

        # Get the ID of the invoice to modify
        id_invoice_modify = request.POST.get('id_modified')

        if id_invoice_modify:
            paid = request.POST.get('modified')

            try:
                # Find the invoice object by ID
                obj = Invoice.objects.get(id=id_invoice_modify)

                # Update the paid status based on the radio button selection
                if paid == 'True':
                    obj.paid = True
                else:
                    obj.paid = False
                obj.save()

                messages.success(request, _('Change made successfully!!'))

            except Invoice.DoesNotExist:
                messages.error(request, _("Invoice not found!"))

            except Exception as e:
                # Handle any other general exceptions
                messages.error(request, f"Sorry.. This error occurred: {e}")


    #Logic to delete an invoice

        id_invoice_delete = request.POST.get('id_supprimer')

        if id_invoice_delete:
            try:
                obj = Invoice.objects.get(pk = id_invoice_delete)
                obj.delete()

                messages.success(request, _('Invoice deleted successfully!!'))
            except Exception as e:
                messages.error(request, f'Sorry.. These errors occurred: {e}')

        items = pagination(request, self.invoices)
        self.context['invoices'] = items
        return render(request, self.template_name, self.context)

class AddCustomerView(LoginRequiredSuperuserMixin, View):

    template_name = 'add_customer.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)
    

    def post(self, request, *args, **kwargs):

        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address'),
            'sex': request.POST.get('sex'),
            'age': request.POST.get('age'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zipcode'),
            'save_by': request.user
        }


        try:
            new_customer = Customer.objects.create(**data)

            if new_customer:
                messages.success(request, _('Customer created successfully!!!'))
            else:
                messages.error(request, _('Sorry! something went wrong..'))


        except Exception as e:
            messages.error(request, f'Sorry!! we detected these errors{e}')
        
        return render(request, self.template_name)
    

class CreateInvoiceView(LoginRequiredSuperuserMixin, View):
        
    template_name = 'create_invoice.html'

    def get(self, request, *args, **kwargs):
        customers = Customer.objects.select_related('save_by').all()
        context = {
            'customers': customers
        }
        return render(request, self.template_name, context)
    
    
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        print(request.POST)
        
        items = []
        total_price = Decimal(0)  # Initialize total price

        try:
            customer = request.POST.get('customer')
            invoice_type = request.POST.get('itype')
            comments = request.POST.get('comment')

            # Loop through all submitted articles
            article_names = request.POST.getlist('article')
            quantities = request.POST.getlist('qty')
            unit_prices = request.POST.getlist('unit')

            for index in range(len(article_names)): 
                article = article_names[index] 
                quantity = Decimal(quantities[index]) if quantities[index] else Decimal(0)
                unit_price = Decimal(unit_prices[index]) if unit_prices[index] else Decimal(0)
                item_total = quantity * unit_price  # Calculate total for each article
                total_price += item_total  # Accumulate total price

                # Create an Article instance for each item
                data = Article(    # creating article_object
                    invoice_id=None,  # Placeholder, will set this after the invoice is created
                    name=article,
                    quantity=quantity,
                    unit_price=unit_price,
                    total=item_total
                )
                items.append(data)

            # Create the invoice object
            invoice_object = {
                'customer_id': customer,
                'save_by': request.user,
                'total': total_price,
                'invoice_type': invoice_type,
                'comments': comments
            }

            new_invoice = Invoice.objects.create(**invoice_object)

            # Assign the invoice_id to each Article and save them
            for item in items:
                item.invoice_id = new_invoice.id  # Set the invoice_id for the article
            Article.objects.bulk_create(items)  # Bulk create articles

            messages.success(request, _('Invoice created successfully!!!'))

        except Exception as e:
            messages.error(request, f'Sorry! these errors occurred {e}')
            return render(request, self.template_name)

        return render(request, self.template_name)      


class ToViewInvoice(View, LoginRequiredSuperuserMixin):

    template_name = 'view_invoice.html'


    def get(self, request, *args, **kwargs):

         pk = kwargs.get('pk')

         context =  seeInvoice(pk)

         return render(request, self.template_name, context)
    
    def post(self, request):
        return render(request, self.template_name)
    

@superuser_required     
def get_invoice_pdf(request, *args, **kwargs):

    pk = kwargs.get('pk')
    context = seeInvoice(pk)
    context['date'] = datetime.datetime.today()

    # Add this line to pass the full URL to static files
    context['static_url'] = request.build_absolute_uri('/static/')

    context['generated_by'] = request.user.username  


     # Generate QR code (you could encode any relevant info, like a URL or ID)
    qr_data = f"Invoice ID: {pk} ~ Issued by: FAEK CORP"  # Customize with relevant data
    qr = qrcode.make(qr_data)
    
    # Save QR code image to a byte stream
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format="PNG")
    
    # Encode the byte stream in base64
    qr_image_base64 = base64.b64encode(qr_buffer.getvalue()).decode("utf-8")
    
    # Add QR code to the context
    context['qr_image'] = qr_image_base64


    #get html file
    template = get_template('invoice_pdf.html')

    #render html with context variables
    html = template.render(context)

    #options of pdf format
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'enable-local-file-access': '',  # Allow access to local files
    }

    # generate pdf 
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type = 'application/pdf')
    response['Content-Disposition'] = 'attachment'
    return response


     
