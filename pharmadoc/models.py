from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Companies"

class DrugClass(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Drug class"


class Pharmacy(models.Model):
    name = models.CharField(max_length=250)
    state = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    active_substance = models.CharField(max_length=250, verbose_name='molecule')
    dose = models.CharField(max_length=250, null=True, verbose_name='concentration')
    drug_class = models.ManyToManyField(DrugClass, related_name='Drug_class',)
    type = models.CharField(max_length=50, choices=(
        ('veterinary', 'veterinary'),
        ('human', 'human'),
        ),)
    animal_species = models.CharField(max_length=250, null=True)
    umwidmungsstufe = models.PositiveIntegerField()
    storage_instructions = models.CharField(max_length=400, null=True, blank=True,)
    comment = models.TextField(blank=True, null=True) 
    attachment = models.FileField(null=True, blank=True, upload_to='uploads/pharmacy/%Y/%m/%d/')
    alarm_value =  models.PositiveIntegerField(null=True, blank=True, help_text="Please enter a number of full containers. If less container are available Alessia gets a mail.") 
    class Meta:
        verbose_name = "Product Info"
        verbose_name_plural = "Product Infos"


    def __str__(self):
        return self.name

    def available_quantity(self):
        products = self.stockproduct_set.all()
        quantity = 0
        for p in products:
            quantity = quantity + p.available_quantity()
        return quantity 
    
    def available_container(self):
        products = self.stockproduct_set.all()
        quantity = 0
        for p in products:
            quantity = quantity + p.available_containers()
        
        return quantity 
    
    def unit(self):
        products = self.stockproduct_set.all()
        i=0
        unit = ''
        for p in products:
            if i == 0:
                unit = p.unit
            else:
                if unit != p.unit:
                    return ('false')
            i = i +1
        return (unit)




class StockProduct (models.Model):
    pharmacy = models.ForeignKey(Pharmacy, null=True, on_delete=models.SET_NULL)
    #company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    state = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    #molecule = models.CharField(max_length=250)
    amount_containers = models.PositiveIntegerField(default=1, verbose_name='Amount of ordered Containers')
    quantity = models.DecimalField(help_text="Quantity of one container",max_digits=10, decimal_places=3,)
    unit = models.CharField(max_length=10, choices=(
        ('ml', 'ml'),
        ('l', 'l'),
        ('mg', 'mg'),
        ('g', 'g'),
        ),)
    delivery_date = models.DateField(null=False)
    expiry_date = models.DateField(null=False)
    batch_number = models.CharField(max_length=250)
    consumed = models.DecimalField(null=True, blank=True,default=0,max_digits=10, decimal_places=3,)
    comment = models.TextField(blank=True, null=True) 
    
    

    def __str__(self):
        text = self.pharmacy.name
        text = text + " " + self.batch_number + " " + str(self.delivery_date)
        return (text)

    def available(self):
        """
        Returns True if the animal is still available
        """
        today = datetime.now().date()
        return (self.expiry_date >= today)

    def delivered_quantity(self):
        return(self.amount_containers * self.quantity)
    
    def available_containers(self):
        submissionlist = Submission.objects.filter(product__pk=self.pk)
        if submissionlist is None:
            return(self.amount_containers)
        quantity = self.quantity
        containers = self.amount_containers
        fullamount = quantity * containers
        realamount = fullamount  
        for s in submissionlist:
            realamount = realamount - s.fullamount()
        if realamount % quantity == 0:
            return (realamount // quantity)
        else:
            return((realamount // quantity)+1)

    def available_quantity(self):
        submissionlist = Submission.objects.filter(product__pk=self.pk)
        if submissionlist is None:
            return(self.amount_containers)
        quantity = self.quantity
        containers = self.amount_containers
        fullamount = quantity * containers
        realamount = fullamount  
        for s in submissionlist:
            realamount = realamount - s.fullamount()
        if realamount == 0:
            state = 'deactivated'
        return(realamount)
    
    def available_quantity_last_container(self):
        submissionlist = Submission.objects.filter(product__pk=self.pk)
        if submissionlist is None:
            return(self.amount_containers)
        quantity = self.quantity
        containers = self.amount_containers
        fullamount = quantity * containers
        realamount = fullamount  
        for s in submissionlist:
            realamount = realamount - s.fullamount()
        if realamount % quantity == 0:
            return (quantity)
        else:
            return(realamount % quantity)


class Person(models.Model):
    name = models.CharField(max_length=250,)
    state = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    def __str__(self):
        return self.name

class Submission(models.Model):
    application_number = models.CharField(max_length=250)
    product = models.ForeignKey(StockProduct, null=True, on_delete=models.SET_NULL)
    date = models.DateField(null=False)
    creation_date = models.DateTimeField(null=False, auto_now_add=True)
    person = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL)
    amount_containers = models.PositiveIntegerField(null=True)
    quantity = models.DecimalField(null=False, default=0,max_digits=10, decimal_places=3,) 
    comment = models.TextField(blank=True, null=True)
    procedure_control = models.CharField(max_length=800,  null=True, blank=True,)
    added_by = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, default=1)
    attachment1 = models.FileField(null=True, blank=True, upload_to='uploads/stockproduct/%Y/%m/%d/')
    attachment2 = models.FileField(null=True, blank=True, upload_to='uploads/stockproduct/%Y/%m/%d/') 

    def fullamount(self):
        if self.amount_containers is None:
            return (self.quantity)
        else:
            return (self.amount_containers * self.product.quantity + self.quantity)
# Create your models here.
