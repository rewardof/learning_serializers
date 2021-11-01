from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=128)
    age = models.IntegerField()
    items_purchased = models.ManyToManyField(Item, through='Purchase')

    def __str__(self):
        return self.name


class Purchase(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_purchased = models.DateField(auto_now_add=True)
    quantity_purchased = models.IntegerField()
