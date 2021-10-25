from django.db import models


class Status(models.Choices):
    OFS = 'Out of stock' # Out of stock
    IS = 'In stock' # In stock
