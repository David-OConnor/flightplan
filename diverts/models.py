from django.db import models


class Navaid(models.Model):
    ident = models.CharField(max_length=6, unique=True)
    name = models.CharField()
    components = models.CharField() # ie ['NDB', 'VOR', 'DME']
    lat = models.FloatField()
    lon = models.FloatField()
    #tac_freq = models.CharField()


class Airfield(models.Model):
    ident = models.CharField(max_length=6, unique=True)
    lat = models.FloatField()
    lon = models.FloatField()
    
    #runways = models.CharField(max_length=500) # serialized as json. {'8-26': 8000, ...}
    runways = models.ManyToManyField('Runway')
    #services = models.CharField(max_length=500)


class Runway(models.Model):
    # Single direction? Ie two entries for rwy 08-26
    id_ = models.IntegerField(unique=True)
    airfield = models.ForeignKey('Airfield')
    length = models.IntegerField()
    heading = models.IntegerField()


class Services(models.Model):
    pass


class Airway(models.Model):
    id_ = models.IntegerField(unique=True)
    navaids = models.CharField(max_length=500)  #ie ['GSB', 'NTR', 'ASD']


class Jetway(Airway):
    pass


class Notam(models.Model):
    pass
