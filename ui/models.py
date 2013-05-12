from django.db import models

class Flowdata(models.Model):
    server = models.CharField(max_length=80)
    protocol = models.SmallIntegerField(db_index=True)
    operation = models.SmallIntegerField(db_index=True)
    filename = models.CharField(max_length=1024, db_index=True)
    start_time = models.DateTimeField('operation start time', db_index=True)
