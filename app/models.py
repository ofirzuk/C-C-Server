from __future__ import unicode_literals
from django.db import models


class Malware(models.Model):
    token = models.CharField(max_length=120, default='')
    teammates = models.CharField(max_length=120, default='')

    def __unicode__(self):
        return self.teammates


class Command(models.Model):
    type = models.CharField(max_length=120, default='')
    value = models.CharField(max_length=200, default='')
    malware = models.ForeignKey(Malware, default=None)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return '%s %s' % (self.malware, self.type)


class DataItem(models.Model):
    name = models.CharField(max_length=200, default='')
    data = models.TextField(default='')
    data_chunks_sent = models.IntegerField(default=1)
    malware = models.ForeignKey(Malware, default=None)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return '%s %s' % (self.malware, self.name)


class FileItem(models.Model):
    name = models.CharField(max_length=200, default='')
    data = models.TextField(default='')
    malware = models.ForeignKey(Malware, default=None)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return '%s %s' % (self.malware, self.name)


