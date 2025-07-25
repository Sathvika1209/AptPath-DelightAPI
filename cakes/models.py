from django.db import models

class Cake(models.Model):
    name = models.CharField(max_length=100)
    flavor = models.CharField(max_length=50)
    size = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Store(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name
