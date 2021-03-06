from django.db import models
from apps.commons.models import BaseModel


class Pricesource(BaseModel):
    registered_name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50)
    data_source = models.CharField(max_length=500, default='')

    def __str__(self):
        return f'{self.short_name}, {self.registered_name}'
