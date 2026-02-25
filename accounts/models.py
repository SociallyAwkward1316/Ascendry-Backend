from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]

    GOAL_CHOICES = [
        ("cut", "Cut"),
        ("maintain", "Maintain"),
        ("bulk", "Bulk"),
    ]

    ACTIVITY = [
        ("sedentary", "Sedentary"),
        ("light", "Light"),
        ("active", "Active"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    weight_lbs = models.IntegerField()
    height_cm = models.IntegerField()
    age = models.IntegerField()

    # nutrition profile ahead
    activity_level = models.CharField(max_length=10, choices=ACTIVITY)
    maintenance_calories = models.IntegerField(null=True, blank=True)
    goal = models.CharField(max_length=10, choices=GOAL_CHOICES)
    calorie_target = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} Profile'


    