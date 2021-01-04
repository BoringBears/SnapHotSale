from django.db import models

# Create your models here.

class DealInfo(models.Model):
    title = models.CharField(max_length=256, verbose_name='Title')
    price = models.CharField(max_length=256, verbose_name='Price')
    price_origin = models.CharField(max_length=256, verbose_name='Original Price')
    link = models.CharField(max_length=256, verbose_name='Link')
    image = models.CharField(max_length=256, verbose_name='Image')
    retailer = models.CharField(max_length=256, verbose_name='Retailer')
    timestamp = models.DateTimeField(max_length=256, verbose_name="Timestamp")
    source = models.CharField(max_length=512, verbose_name='Source')

    def __str__(self):
        return "{}-{}-{}".format(self.title,self.price, self.link)

    class Meta:
        verbose_name = "Show Deals"



