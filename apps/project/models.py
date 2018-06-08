from django.db import models

class IT_Project(models.Model):

    project_name = models.CharField(max_length=30)
    project_description = models.CharField(max_length=30)
    client_id = models.IntegerField()
    project_manager_id = models.IntegerField()
    project_price = models.IntegerField()
    project_start_date_time = models.DateTimeField()
    project_end_date_time = models.DateTimeField()
    project_total_working_hr = models.IntegerField()
    project_total_time_taken = models.IntegerField()





