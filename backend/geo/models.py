from django.db import models


class Country(models.Model):
    name = models.CharField('name', max_length=255)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField('name', max_length=255)
    abbreviation = models.CharField('abbreviation', max_length=10)
    country = models.ForeignKey(
        'geo.Country',
        on_delete=models.CASCADE,
        related_name='state_set',
        related_query_name='state'
    )

    def __str__(self):
        return self.name


class Address(models.Model):
    address = models.CharField(
        'address',
        max_length=255,
        blank=True,
        null=True
    )
    country = models.ForeignKey(
        'geo.Country',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    city = models.ForeignKey(
        'geo.City',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    zip = models.ForeignKey(
        'geo.Zip',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.address or ''


class City(models.Model):
    name = models.CharField('name', max_length=255)
    state = models.ForeignKey(
        'geo.State',
        on_delete=models.CASCADE,
        related_name='cities',
        related_query_name='city'
    )
    timezone = models.CharField(
        'timezone',
        max_length=255,
        default='UTC'
    )

    class Meta:
        unique_together = ('name', 'state')
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Zip(models.Model):
    code = models.CharField('code', max_length=32)
    city = models.ForeignKey(
        'geo.City', on_delete=models.CASCADE,
        related_name='zips'
    )

    def __str__(self):
        return self.code
