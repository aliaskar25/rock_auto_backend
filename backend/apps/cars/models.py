from django.db import models

from .choices import Status


class Country(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name


class Mark(models.Model):
    name = models.CharField(max_length=128)
    countries = models.ManyToManyField(
        Country, blank=True, related_name='marks'
    )

    def __str__(self):
        return self.name


class Year(models.Model):
    year = models.PositiveIntegerField()
    mark = models.ForeignKey(
        Mark, on_delete=models.CASCADE, related_name='years'
    )
    countries = models.ManyToManyField(
        Country, blank=True, related_name='years'
    )
    
    def __str__(self):
        return f'{self.mark} {self.year}'


class MarkModel(models.Model):
    name = models.CharField(max_length=128)
    year = models.ForeignKey(
        Year, on_delete=models.CASCADE, related_name='mark_models'
    )

    def __str__(self):
        return self.name


class Complectation(models.Model):
    name = models.CharField(max_length=128)
    mark_model = models.ForeignKey(
        MarkModel, on_delete=models.CASCADE, related_name='complectations'
    )

    def __str__(self):
        return self.name

    
class Detail(models.Model):
    name = models.CharField(max_length=128)
    complectation = models.ForeignKey(
        Complectation, on_delete=models.CASCADE, related_name='details'
    )

    def __str__(self):
        return self.name


class SubDetail(models.Model):
    name = models.CharField(max_length=128)
    detail = models.ForeignKey(
        Detail, on_delete=models.CASCADE, related_name='sub_details'
    )

    def __str__(self):
        return self.name


class Part(models.Model):
    name = models.CharField(max_length=1024)
    price = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.IS
    )
    sub_detail = models.ForeignKey(
        SubDetail, on_delete=models.CASCADE, related_name='parts'
    )

    def __str__(self):
        return self.name


class PartVariety(models.Model):
    name = models.CharField(max_length=1024)
    price = models.FloatField(null=True, blank=True)
    part = models.ForeignKey(
        Part, on_delete=models.CASCADE, related_name='varieties'
    )

    def __str__(self):
        return f'{self.part.name} {self.name}'
