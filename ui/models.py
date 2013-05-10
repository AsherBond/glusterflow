from django.db import models

# This could really use index creation here, as they make a big
# difference.  (I've been manually adding them using psql so far)
class Flowdata(models.Model):
    server = models.CharField(max_length=80)
    protocol = models.CharField(max_length=6)
    operation = models.CharField(max_length=12)
    filename = models.CharField(max_length=1024)
    start_time = models.DateTimeField('operation start time')
