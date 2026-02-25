from rest_framework import serializers
from .models import Workout, WorkoutExercise, Set, Exercise, MuscleGroup

class CreateWorkoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workout
        fields = ['name']

    def create(self, validated_data):
        user = self.context.get("user")
        workout = Workout.objects.create(
            user=user,
            name=validated_data["name"]
        )
        return workout
    

class CreateExerciseSerializer(serializers.ModelSerializer):

    muscle_groups = serializers.PrimaryKeyRelatedField(many=True, queryset=MuscleGroup.objects.all())

    class Meta:
        model = Exercise
        fields = ['name', 'muscle_groups', 'is_custom']

    def create(self, validated_data):
        muscle_groups = validated_data.pop("muscle_groups")
        user = self.context.get("user")

        exercise = Exercise.objects.create(
            name=validated_data["name"],
            is_custom=validated_data["is_custom"],
            created_by=user if validated_data["is_custom"] == True else None
        )
        exercise.muscle_groups.set(muscle_groups)
        return exercise

    

class CreateWorkoutExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutExercise
        fields = ["workout", "exercise"]

    def create(self, validated_data):
        workout = self.context.get("workout")
        exercise = self.context.get("exercise")
        order = self.context.get("order")
        workoutexercise = WorkoutExercise.objects.create(
            workout=workout,
            exercise=exercise,
            order=order
        )
        return workoutexercise
    

class CreateSetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Set
        fields = ['workout_exercise', 'set_number', 'reps', 'weight']

    def create(self, validated_data):
        workout_exercise = self.context.get('workout_exercise')

        create_set = Set.objects.create(
            workout_exercise=workout_exercise,
            set_number=validated_data['set_number'],
            reps=validated_data['reps'],
            weight=validated_data['weight']

        )

        return create_set
    

#----------List-Serializers----------#
class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ["id", "set_number", "reps", "weight"]

class WorkoutListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Workout
        fields = ['name', 'performed_at']


class WorkoutExerciseListSerializer(serializers.ModelSerializer):
    sets = SetSerializer(many=True, read_only=True)
    exercise_name = serializers.CharField(source="exercise.name", read_only=True)
    class Meta:
        model = WorkoutExercise
        fields = ['id','exercise','exercise_name','order', 'sets']


class ExerciseListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'muscle_groups', 'is_custom']
#----------Update-Serializers---------#
class UpdateWorkoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workout
        fields = ['name']


class UpdateSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Set
        fields = ['set_number', 'reps', 'weight']