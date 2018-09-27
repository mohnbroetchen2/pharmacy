from django.db import models
from datetime import datetime

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
    amount_containers = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(help_text="Quantity of one container")
    unit = models.CharField(max_length=10, choices=(
        ('ml', 'ml'),
        ('g', 'g'),
        ),)
    delivery_date = models.DateField(null=False)
    expiry_date = models.DateField(null=False)
    batch_number = models.CharField(max_length=250)
    consumed = models.PositiveIntegerField(null=True, blank=True,default=0)
    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=250,)
    def __str__(self):
        return self.name

class Submission(models.Model):
    application_number = models.CharField(max_length=250)
    pharmacy = models.ForeignKey(Pharmacy, null=True, on_delete=models.SET_NULL)
    date = models.CharField(max_length=250)
    person = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL)
    amount_containers = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(help_text="Quantity of one container") 
    comment = models.TextField(blank=True, null=True)
    procedure_control = models.CharField(max_length=250,  null=True, blank=True)



# Create your models here.
