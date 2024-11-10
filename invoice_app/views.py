from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from .utils import pagination

# Create your views here.
class HomeView(View):
    """ Main/Home view """

    template_name = 'index.html'

    invoices = Invoice.objects.select_related('customer', 'save_by').all().order_by('-invoice_date') 

    context = {
            'invoices': invoices
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

                messages.success(request, 'Change made successfully!!')

            except Invoice.DoesNotExist:
                messages.error(request, "Invoice not found!")

            except Exception as e:
                # Handle any other general exceptions
                messages.error(request, f"Sorry.. This error occurred: {e}")


    #Logic to delete an invoice

        id_invoice_delete = request.POST.get('id_supprimer')

        if id_invoice_delete:
            try:
                obj = Invoice.objects.get(pk = id_invoice_delete)
                obj.delete()

                messages.success(request, 'Invoice deleted successfully!!')
            except Exception as e:
                messages.error(request, 'Sorry.. These errors occurred: {e}')

        items = pagination(request, self.invoices)
        self.context['invoices'] = items
        return render(request, self.template_name, self.context)

class AddCustomerView(View):

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
                messages.success(request, 'Customer created successfully!!!')
            else:
                messages.error(request, 'Sorry! something went wrong..')


        except Exception as e:
            messages.error(request, f'Sorry!! we detected these errors{e}')
        
        return render(request, self.template_name)
    

class CreateInvoiceView(View):
        
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

            messages.success(request, 'Invoice created successfully!!!')

        except Exception as e:
            messages.error(request, f'Sorry! these errors occurred {e}')
            return render(request, self.template_name)

        return render(request, self.template_name)      


class ToViewInvoice(View):

    template_name = 'view_invoice.html'

    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')

        obj = Invoice.objects.get(id=pk)

        articles = obj.article_set.all()

        context = {
            'articles': articles,
            'obj': obj,
        }


        return render(request,self.template_name, context)
    
    def post(self, request):
        return render(request, self.template_name)

     
