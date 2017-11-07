from django.db import models


class Location(models.Model):
    lat = models.CharField(max_length=10)
    lng = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    
    class Meta:
        unique_together = ['lat', 'lng']
    
    def __str__(self):
        return self.address
