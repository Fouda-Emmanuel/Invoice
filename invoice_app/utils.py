from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def pagination(request, invoices):
    
        default_page = 1

        page = request.GET.get('page', default_page)

        items_per_page = 4

        paginator = Paginator(invoices, items_per_page)

        try:
            item_page = paginator.page(page)

        except PageNotAnInteger:
            item_page = paginator.page(default_page)
        
        except EmptyPage:
            item_page = paginator.page(paginator.num_pages)

        return item_page