from django.db import models

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)


class Content(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    content = models.TextField()
    value = models.FloatField(default=100)

    def get_content(user, x=3):   
        return Content.objects.filter(customer = user).order_by('-value')[:x]
