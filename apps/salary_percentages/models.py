from django.db import models

class Salary_Structure(models.Model):

    financial_year = models.CharField(max_length=4,null=True,blank=True)
    hra_percentage = models.FloatField(null=True,blank=True)
    dearness_percentage=models.FloatField(null=True,blank=True)
    pf_percentage = models.FloatField(null=True,blank=True)
    medical_allowance = models.FloatField(null=True,blank=True)
    conveyance_allowance = models.FloatField(null=True,blank=True)
    washing_allowance=models.FloatField(null=True,blank=True)
    other_allowance_percentage= models.FloatField(null=True,blank=True)
    max_bonus_percentage=models.FloatField(null=True,blank=True)

    def __str__(self):
        return "%d" % (self.financial_year)

    class Meta:
        permissions = (
            ('view_Salary_Structure', 'Can view salary structure'),
        )



