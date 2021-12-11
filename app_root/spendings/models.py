from django.db import models


class SpendingORM(models.Model):
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=3)
    description = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {} {}".format(self.description, self.amount, self.currency)
