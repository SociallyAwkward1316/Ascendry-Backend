from django.contrib import admin
from .models import MuscleGroup, Workout, Exercise, WorkoutExercise, Set

# Register your models here.
admin.site.register(MuscleGroup)
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(WorkoutExercise)
