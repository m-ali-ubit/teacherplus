from django.db import models
from django_countries.fields import CountryField


class Country(models.Model):
    country = CountryField(multiple=False, blank=True)

    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name_plural = "Countries"


class City(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"
