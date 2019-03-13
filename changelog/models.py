from django.db import models

class Change(models.Model):
    change_type = models.CharField(max_length=100, choices=(
        ('new', 'new'),
        ('adaption', 'adaption'),
        ('bugfix', 'bugfix'),
        ('deletion', 'deletion'),
    ), default="adaption")
    version = models.CharField(max_length=200, )
    entry_date = models.DateField(null=False, auto_now_add=True)
    short_text = models.CharField(max_length=400, )
    description = models.TextField(blank=True, null=True, )
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    def __str__(self):
        return self.change_type

    """def __str__(self):
        return "{} {} {}, {} id:{} [{}]".format
        (self.version, self.change_type, self.short_text, self.description, self.pk, self.entry_date)
    """
