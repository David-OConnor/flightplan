from django.db import models


class Airfield(models.Model):
    # Airfield idents have 3 or 4 characters.
    ident = models.CharField(max_length=4, primary_key=True)
    # Airfield icaos always have 4 characters.
    # Can't be unique, since some airfields don't have one. If there is one, it's always 4 chars.
    icao = models.CharField(max_length=4)
    # The AIXM unique identifier, used for tieing runways to airfields.
    aixm_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return ', '.join([self.ident, self.name])
    
    #services = models.CharField(max_length=500)


class Runway(models.Model):
    # Single direction? Ie two entries for rwy 08-26
    airfield = models.ForeignKey(Airfield)
    number = models.CharField(max_length=50)  # ie '04/26' or '04'
    length = models.IntegerField()  # feet
    width = models.IntegerField()  # feet
    # Common characteristics are 'WATER', 'GRASS', and 'ASPH'
    surface = models.CharField(max_length=30)

    def __str__(self):
        return ', '.join([str(self.airfield), self.number])


class Navaid(models.Model):
    # Navaids have 1 to 3 characters.
    ident = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100)
    components = models.CharField(max_length=500)  # ie ['NDB', 'VOR', 'DME']
    lat = models.FloatField()
    lon = models.FloatField()
    #tac_freq = models.CharField()

    def __str__(self):
        return self.ident


class Fix(models.Model):
    # Fixes always have 5 characters.
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
