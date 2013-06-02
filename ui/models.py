from django.db import models

class Flowdata_New(models.Model):
    server = models.CharField(max_length=80)
    protocol = models.SmallIntegerField(db_index=True)
    operation = models.SmallIntegerField(db_index=True)
    filename = models.CharField(max_length=1024, db_index=True)
    start_time = models.DateTimeField('operation start time', db_index=True)

class Flowdata_Archive(models.Model):
    server = models.CharField(max_length=80)
    protocol = models.SmallIntegerField()
    operation = models.SmallIntegerField()
    filename = models.CharField(max_length=1024)
    start_time = models.DateTimeField('operation start time')

class Fop_Summaries(models.Model):
    server = models.CharField(max_length=80, db_index=True)
    operation = models.SmallIntegerField(db_index=True)
    summary_time = models.DateTimeField('time of summary', db_index=True)
    count = models.SmallIntegerField(db_index=False)

class Filename_Summaries(models.Model):
    server = models.CharField(max_length=80, db_index=True)
    filename = models.CharField(max_length=1024, db_index=True)
    summary_time = models.DateTimeField('time of summary', db_index=True)
    count = models.SmallIntegerField(db_index=False)
