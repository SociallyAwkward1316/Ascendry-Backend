from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from .serializers import (CreateWorkoutSerializer, CreateWorkoutExerciseSerializer, CreateSetSerializer, CreateExerciseSerializer, WorkoutListSerializer,
    WorkoutExerciseListSerializer, ExerciseListSerializer)
from .serializers import UpdateWorkoutSerializer, UpdateSetSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from .pagination import StandardPagination

from.models import Workout, Exercise, WorkoutExercise, Set

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateWorkout(request):
    serializer = CreateWorkoutSerializer(data=request.data, context={"user":request.user})
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateExercise(request):
    serializer = CreateExerciseSerializer(data=request.data, context={"user":request.user})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateWorkoutExercise(request, workout_id, exercise_id):
    workout = get_object_or_404(Workout, pk=workout_id, user=request.user)
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    order = WorkoutExercise.objects.filter(workout=workout).count() + 1

    serializer = CreateWorkoutExerciseSerializer(data=request.data, context={"workout":workout, "exercise":exercise, "order":order})
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateSet(request, WorkoutExercise_id):
    workout_exercise = get_object_or_404(WorkoutExercise, pk=WorkoutExercise_id, workout__user=request.user)
    serializer = CreateSetSerializer(data=request.data, context={'workout_exercise':workout_exercise})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#------Endpoints for listing---------#


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def AllWorkoutList(request):
    user_workouts = Workout.objects.filter(user=request.user)
    serializer = WorkoutListSerializer(user_workouts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def WorkoutExerciseList(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id, user=request.user)
    workout_exercise_list = WorkoutExercise.objects.filter(workout=workout).select_related("exercise").prefetch_related("sets")
    serializer = WorkoutExerciseListSerializer(workout_exercise_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ExerciseList(request):
    exercises = Exercise.objects.filter(Q(is_custom=False)| Q(created_by=request.user)).order_by("name")

    paginator = StandardPagination()
    paginated_queryset = paginator.paginate_queryset(exercises, request)
    serializer = ExerciseListSerializer(paginated_queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
#-----------Endpoints for Updating-------#


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def UpdateWorkout(request, workout_id):
    partial = request.method == "PATCH"
    workout = get_object_or_404(Workout, pk=workout_id, user=request.user)
    serializer = UpdateWorkoutSerializer(workout, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT','PATCH'])
@permission_classes([IsAuthenticated])
def UpdateSet(request, set_id):
    partial = request.method == "PATCH"
    set_obj = get_object_or_404(Set, pk=set_id, workout_exercise__workout__user=request.user)
    serializer = UpdateSetSerializer(set_obj, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#-----------Endpoints for Deletion-------#

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteWorkout(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id, user=request.user)
    workout.delete()
    return Response({"Success":True}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteExercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id, created_by=request.user)
    exercise.delete()
    return Response({"Success":True}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteWorkoutExercise(request, workout_exercise_id):
    workout_exercise = get_object_or_404(WorkoutExercise, pk=workout_exercise_id, workout__user=request.user)
    workout = workout_exercise.workout
    workout_exercise.delete()

    #---Reorder after deletion----#
    remaining = WorkoutExercise.objects.filter(workout=workout).order_by('order')
    for index, item in enumerate(remaining, start=1):
        item.order = index
        item.save()
    return Response({"Success":True}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteSet(request, set_id):
    set_obj = get_object_or_404(Set, pk=set_id, workout_exercise__workout__user=request.user)
    set_obj.delete()
    return Response({"Success":True}, status=status.HTTP_200_OK)
