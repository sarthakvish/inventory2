from django.db import models
from django.utils import timezone


class Purchase(models.Model):
    item_name = models.CharField(max_length=50, blank=True, null=True)
    price=models.PositiveIntegerField()
    quantity=models.PositiveIntegerField()
    total_price=models.PositiveIntegerField(blank=True)
    provider_name = models.CharField(max_length=255)
    provider_contact = models.CharField(max_length=255, unique=True)
    date=models.DateTimeField(default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        self.total_price= self.price*self.quantity
        super().save(*args, *kwargs)

    def __str__(self):
        return "Sailed {}-{} for {}".format(self.item_name, self.quantity, self.total_price)


