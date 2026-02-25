from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MuscleGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    performed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=50)
    muscle_groups = models.ManyToManyField(MuscleGroup)
    is_custom = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="exercises")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.IntegerField()

    def __str__(self):
        return self.exercise.name


class Set(models.Model):
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE, related_name="sets")
    set_number = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.FloatField()

    def __str__(self):
        return f'{self.set_number} x {self.reps}'
    

