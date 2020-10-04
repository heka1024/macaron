from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    code = models.SmallIntegerField(unique=True)

    time_breakfast = models.CharField(max_length=50, blank=True, default="")
    time_lunch = models.CharField(max_length=50, blank=True, default="")
    time_dinner = models.CharField(max_length=50, blank=True, default="")

    menus = models.ForeignKey(Menu, related_name="restaurant", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Restaurant({self.name}, {self.code})"
