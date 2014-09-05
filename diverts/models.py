from django.db import models


class Navaid(models.Model):
    ident = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=100)
    components = models.CharField(max_length=500)  # ie ['NDB', 'VOR', 'DME']
    lat = models.FloatField()
    lon = models.FloatField()
    #tac_freq = models.CharField()

    def __str__(self):
        return self.ident


class Airfield(models.Model):
    ident = models.CharField(max_length=6, primary_key=True)
    # The AIXM unique identifier, used for tieing runways to airfields.
    aixm_id = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    # control = models.CharField(max_length=100)  #'CIVIL', or ... MILITARY?  #todo remove this
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return self.ident
    
    #services = models.CharField(max_length=500)


class Runway(models.Model):
    # Single direction? Ie two entries for rwy 08-26
    airfield = models.ForeignKey(Airfield)
    number = models.CharField(max_length=50)  # ie '04/26' or '04'
    length = models.IntegerField()  # feet
    width= models.IntegerField()  # feet

    def __str__(self):
        return str(self.airfield) + ' ' + self.number


class Services(models.Model):
    pass


class Airway(models.Model):
    navaids = models.CharField(max_length=500)  #ie ['GSB', 'NTR', 'ASD']


class Jetway(Airway):
    pass


class Notam(models.Model):
    pass
