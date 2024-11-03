from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):

    SEX_TYPES = (
        ('M', 'Masculin'),
        ('F', 'Feminin'),
    )

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    sex = models.CharField(max_length=1, choices=SEX_TYPES)
    age = models.CharField(max_length=20)
    city = models.CharField(max_length=40)
    zip_code = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
    

class Invoice(models.Model):

    INVOICE_TYPE = (
        ('R', 'RECU'),
        ('P', 'PROFORMA'),
        ('F', 'FACTURE'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)
    invoice_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=20000, decimal_places=2)
    last_updated_time = models.DateTimeField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    invoice_type = models.CharField(max_length=1, choices=INVOICE_TYPE)
    comments = models.TextField(max_length=1000, null=True, blank=True)

    @property
    def get_total(self):
        articles = self.article_set.all()
        total = sum(article.total_article for article in articles)
        return total

    def __str__(self):
        return f'{self.customer.name}_{self.invoice_date}'
    
class Article(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=1000, decimal_places=2)
    total= models.DecimalField(max_digits=1000, decimal_places=2)

    @property
    def total_article(self):
        return self.quantity * self.unit_price
    
    def __str__(self):
        return self.name