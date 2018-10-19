from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name

class DrugClass(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name


class Pharmacy(models.Model):
    name = models.CharField(max_length=250)
    state = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    molecule = models.CharField(max_length=250)
    drug_class = models.ManyToManyField(DrugClass, related_name='Drug_class',)
    type = models.CharField(max_length=50, choices=(
        ('veterinary', 'veterinary'),
        ('human', 'human'),
        ),)
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)


    def __str__(self):
        return self.name

class Product (models.Model):
    name = models.CharField(null=True, blank=True, max_length=250)
    pharmacy = models.ForeignKey(Pharmacy, null=True, on_delete=models.SET_NULL)
    state = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    amount_containers = models.PositiveIntegerField(default=1)
    quantity = models.PositiveIntegerField(help_text="Quantity of one container")
    unit = models.CharField(max_length=10, choices=(
        ('ml', 'ml'),
        ('g', 'g'),
        ),)
    delivery_date = models.DateField(null=False)
    expiry_date = models.DateField(null=False)
    batch_number = models.CharField(max_length=250)
    consumed = models.PositiveIntegerField(null=True, blank=True,default=0)
    comment = models.TextField(blank=True, null=True)    
    

    def __str__(self):
        return self.batch_number

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
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date = models.DateField(null=False)
    creation_date = models.DateTimeField(null=False, auto_now_add=True)
    person = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL)
    amount_containers = models.PositiveIntegerField(null=True)
    quantity = models.PositiveIntegerField(null=False, default=0,) 
    comment = models.TextField(blank=True, null=True)
    procedure_control = models.CharField(max_length=250,  null=True, blank=True)
    added_by = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, default=1)

    def fullamount(self):
        if self.amount_containers is None:
            return (self.quantity)
        else:
            return (self.amount_containers * self.product.quantity + self.quantity)
# Create your models here.
