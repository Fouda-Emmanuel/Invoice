from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib import messages

# Create your views here.
class HomeView(View):
    """ Main/Home view """

    template_name = 'index.html'
    

    invoices = Invoice.objects.select_related('customer', 'save_by').all() 

    context = {
        'invoices': invoices
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context) 


    def post(self, request, *args, **kwargs):
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
    
    
