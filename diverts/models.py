from django.db import models

#todo sort out the extra char airfields and navaids. Sould always be len 4, 3 repsectively

class Airfield(models.Model):
    ident = models.CharField(max_length=5, primary_key=True)
    # The AIXM unique identifier, used for tieing runways to airfields.
    aixm_id = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return self.ident + self.name
    
    #services = models.CharField(max_length=500)


class Runway(models.Model):
    # Single direction? Ie two entries for rwy 08-26
    airfield = models.ForeignKey(Airfield)
    number = models.CharField(max_length=50)  # ie '04/26' or '04'
    length = models.IntegerField()  # feet
    width= models.IntegerField()  # feet

    def __str__(self):
        return str(self.airfield) + ' ' + self.number


class Navaid(models.Model):
    ident = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=100)
    components = models.CharField(max_length=500)  # ie ['NDB', 'VOR', 'DME']
    lat = models.FloatField()
    lon = models.FloatField()
    #tac_freq = models.CharField()

    def __str__(self):
        return self.ident


class Fix(models.Model):
    ident = models.CharField(max_length=5, primary_key=True)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return self.ident


class Services(models.Model):
    pass


class Airway(models.Model):
    navaids = models.CharField(max_length=500)  #ie ['GSB', 'NTR', 'ASD']


class Jetway(Airway):
    pass


class Notam(models.Model):
    pass
