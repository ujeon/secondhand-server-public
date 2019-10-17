from django.conf import settings
from django.db import models


class Raw_data(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    price = models.IntegerField()
    url = models.URLField(max_length=200)
    img_url = models.TextField()
    market = models.CharField(max_length=10)
    posted_at = models.DateField()
    is_sold = models.BooleanField()
    category = models.ForeignKey("Category", on_delete=models.PROTECT)
    location = models.CharField(max_length=60)

    def __str__(self):
        return self.title


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=60)

    def __str__(self):
        return self.category_name


class Filtered_data(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=60)
    model = models.CharField(max_length=60)
    price = models.IntegerField()
    url = models.URLField(max_length=200)
    img_url = models.TextField()
    market = models.CharField(max_length=10)
    posted_at = models.DateField()
    is_sold = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    location = models.CharField(max_length=60)

    def __str__(self):
        return "user_data: {} {} {} ".format(self.id, self.brand, self.model)


class Average_price(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=60)
    model = models.CharField(max_length=60)
    date = models.DateField()
    average_price = models.IntegerField()
    lowest_price = models.IntegerField()
    highest_price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.brand

