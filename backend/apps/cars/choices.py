from django.db import models


class Status(models.Choices):
    OOS = 'Out of stock' # Out of stock
    IS = 'In stock' # In stock
