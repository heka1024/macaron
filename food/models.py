from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    code = models.SmallIntegerField(unique=True)

    time_breakfast = models.CharField(max_length=50, blank=True, default="")
    time_lunch = models.CharField(max_length=50, blank=True, default="")
    time_dinner = models.CharField(max_length=50, blank=True, default="")

    # menus = models.ForeignKey(Menu, related_name="restaurant", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Restaurant({self.name}, {self.code})"

class Menu(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    date = models.DateField()
    TIME = (
        (0, 'ALL'),
        (1, 'BREAKFAST'),
        (2, 'LUNCH'),
        (3, 'DINNER')
    )
    time = models.SmallIntegerField(choices=TIME, default=0)
    date = models.DateField()

    without_fork = models.BooleanField(default=False)
    is_vegetarian = models.BooleanField(default=False)

    restaurant = models.ForeignKey(Restaurant, related_name='menus', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Menu({self.name}, {self.price})"
