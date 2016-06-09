__author__ = 'rabia'
from django.db import models


class Table(models.Model):
    title = models.CharField(max_length=20)
    seats_count = models.IntegerField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title