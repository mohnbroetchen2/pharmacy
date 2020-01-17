from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
import os

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

class Molecule(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name

class Pharmacy(models.Model):
    name = models.CharField(max_length=250)
    state = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    #molecule = models.ForeignKey(Molecule, null=False, on_delete=models.CASCADE) 
    molecule = models.ManyToManyField(Molecule, related_name='molecule_class',)
    company = models.ForeignKey(Company, null=False, on_delete=models.CASCADE)
    drug_class = models.ManyToManyField(DrugClass, related_name='Drug_class',)
    dose = models.CharField(max_length=250, null=False, verbose_name='concentration active substance')
    type = models.CharField(max_length=50, choices=(
        ('veterinary', 'veterinary'),
        ('human', 'human'),
        ),)
    animal_species = models.CharField(max_length=250, null=True)
    umwidmungsstufe = models.PositiveIntegerField()
    storage_instructions = models.CharField(max_length=400, null=True, blank=True,)
    comment = models.TextField(blank=True, null=True) 
    attachment = models.FileField(null=True, blank=True, upload_to='uploads/pharmacy/%Y/%m/')
    alarm_value =  models.PositiveIntegerField(null=True, blank=True, help_text="Please enter a number of full containers. If less container are available Alessia gets a mail.") 
    class Meta:
        verbose_name = "Product Info"
        verbose_name_plural = "Product Infos"

    def get_molecule(self):
        return ",\n".join([ot.name for ot in self.molecule.all()])
    
    def get_drug_class(self):
        """Get all organ types which are used"""
        return ", ".join([dc.name for dc in self.drug_class.all()])
        
    @property
    def attachment_name(self):
        return os.path.basename(self.attachment.name)


    def __str__(self):
        return (self.name + " " + self.dose)

    def available_quantity_date(self, Date):
        products = self.order_set.all()
        quantity = 0
        for p in products:
            if p.state == 'active':
                quantity = quantity + p.available_quantity_date(Date=Date)
        return quantity

    def available_quantity(self):
        products = self.order_set.all()
        quantity = 0
        for p in products:
            if p.state == 'active':
                quantity = quantity + p.available_quantity()
        return quantity 
    
    def available_container(self):
        products = self.order_set.all()
        quantity = 0
        for p in products:
            if p.state == 'active':
                quantity = quantity + p.available_containers()
        
        return quantity 
    
    def unit(self):
        products = self.order_set.all()
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

#class StockProduct (models.Model):
class Order (models.Model):
    identifier = models.CharField(max_length=50)
    pharmacy = models.ForeignKey(Pharmacy, null=True, on_delete=models.SET_NULL)
    #company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    state = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    #molecule = models.CharField(max_length=250)
    
    amount_containers = models.PositiveIntegerField(default=1, verbose_name='Amount ordered Containers')
    quantity = models.DecimalField(help_text="Quantity of one container",max_digits=10, decimal_places=3,verbose_name='Quantity one container')
    unit = models.CharField(max_length=10, choices=(
        ('ml', 'ml'),
        ('l', 'l'),
        ('mg', 'mg'),
        ('g', 'g'),
        ('pill', 'pill'),
        ),)
    delivery_date = models.DateField(null=False)
    expiry_date = models.DateField(null=False)
    batch_number = models.CharField(max_length=250)
    attachment = models.FileField(null=True, blank=True, upload_to='uploads/pharmacy/order/%Y/%m/')
    comment = models.TextField(blank=True, null=True) 

    def save(self, *args, **kwargs):
        if not self.pk: # Only set identifier during the first save.
            stringdate = str(self.delivery_date)
            new_identifier =  self.pharmacy.name[:3] + stringdate[2:] 
            existingOrder = Order.objects.filter(identifier=new_identifier)
            if existingOrder:
                found = 1
                i=2
                while found == 1: 
                    temp_identifier =new_identifier+"_"+str(i)
                    existingOrder = Order.objects.filter(identifier=temp_identifier)
                    if existingOrder:
                        i=i+1
                    else:
                        found = 0
                self.identifier = new_identifier+"_"+str(i)
            else:
                self.identifier = new_identifier

        return super(Order, self).save(*args, **kwargs)
    
    

    def __str__(self):
        text = self.pharmacy.name
        text = text + " " +self.identifier
        return (text)

    def available(self):
        """
        Returns True if order is not expired
        """
        today = datetime.now().date()
        return (self.expiry_date >= today)

    def delivered_quantity(self):
        return(self.amount_containers * self.quantity)

    def available_containers(self):
        submissionlist = Submission.objects.filter(order__pk=self.pk)
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

    def available_quantity_date(self, Date):
        submissionlist = Submission.objects.filter(order__pk=self.pk)
        if submissionlist is None:
            return(self.amount_containers)
        quantity = self.quantity
        containers = self.amount_containers
        fullamount = quantity * containers
        realamount = fullamount
        for s in submissionlist:
            if s.date >= Date: #datetime.date(datetime.strptime(Date, '%Y-%m-%d')): #convert string to datetime and datetime to date
                realamount = realamount - s.fullamount() #amount now minus all submission ever since the date
        return(realamount)

    def available_quantity(self):
        submissionlist = Submission.objects.filter(order__pk=self.pk)
        if submissionlist is None:
            return(self.amount_containers)
        quantity = self.quantity
        containers = self.amount_containers
        fullamount = quantity * containers
        realamount = fullamount  
        for s in submissionlist:
            realamount = realamount - s.fullamount()
        if realamount == 0:
            self.state = 'deactivated'
            self.save()
        return(realamount)
    
    def available_quantity_last_container(self):
        submissionlist = Submission.objects.filter(order__pk=self.pk)
        if submissionlist is None:
            return(self.amount_containers)
        quantity = self.quantity
        containers = self.amount_containers
        fullamount = quantity * containers
        realamount = fullamount  
        for s in submissionlist:
            realamount = realamount - s.fullamount()
        #if realamount == quantity:
        #    self.state = 'deactivated'
        #    self.save()
        #    return(0)
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
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    date = models.DateField(null=False)
    creation_date = models.DateTimeField(null=False, auto_now_add=True)
    person = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL)
    amount_containers = models.PositiveIntegerField(null=True)
    quantity = models.DecimalField(null=False, default=0,max_digits=10, decimal_places=3,) 
    comment = models.TextField(blank=True, null=True)
    procedure_control = models.CharField(max_length=800,  null=True, blank=True,)
    added_by = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, default=1)
    attachment1 = models.FileField(null=True, blank=True, upload_to='uploads/order/%Y/%m/%d/')
    attachment2 = models.FileField(null=True, blank=True, upload_to='uploads/order/%Y/%m/%d/') 

    def fullamount(self):
        if self.amount_containers is None:
            return (self.quantity)
        else:
            return (self.amount_containers * self.order.quantity + self.quantity)

