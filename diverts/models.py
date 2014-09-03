from django.db import models


class Navaid(models.Model):
    ident = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=100)
    components = models.CharField(max_length=500)  # ie ['NDB', 'VOR', 'DME']
    lat = models.FloatField()
    lon = models.FloatField()
    #tac_freq = models.CharField()


class Airfield(models.Model):
    ident = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=100)  #todo implement name after resetting db or migration etc
    control = models.CharField(max_length=100)  #'CIVIL', or ... MILITARY?
    lat = models.FloatField()
    lon = models.FloatField()
    
    #runways = models.CharField(max_length=500) # serialized as json. {'8-26': 8000, ...}
    runways = models.ManyToManyField('Runway', related_name='airfield_rwys')  #figure out what related name should be
    #services = models.CharField(max_length=500)


class Runway(models.Model):
    # Single direction? Ie two entries for rwy 08-26
    airfield = models.ForeignKey('Airfield')
    number = models.CharField(max_length=50)  # ie '04/26' or '04'
    length = models.IntegerField()  # feet
    width= models.IntegerField()  # feet


class Services(models.Model):
    pass


class Airway(models.Model):
    navaids = models.CharField(max_length=500)  #ie ['GSB', 'NTR', 'ASD']


class Jetway(Airway):
    pass


class Notam(models.Model):
    pass
