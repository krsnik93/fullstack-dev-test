from django.db import models

class Seller(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

class SellerHandle(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
