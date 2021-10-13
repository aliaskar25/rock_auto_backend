from django.db import models


class Mark(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Year(models.Model):
    year = models.PositiveIntegerField()
    mark = models.ForeignKey(
        Mark, on_delete=models.CASCADE, related_name='years'
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
