from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from .account_logic import calculate_maintenance_calories, calculate_calorie_goal

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],

        )
        user.set_password(validated_data['password'])
        user.save()


        return user
    

class ProfileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['gender', 'weight_lbs', 'height_cm', 'age', 'goal', 'activity_level', 'maintenance_calories', 'calorie_target']

    def create(self, validated_data):
        maintenance_calories = calculate_maintenance_calories(validated_data['weight_lbs'], validated_data['height_cm'], validated_data['age'], validated_data['gender'], validated_data['activity_level'])
        calorie_target = calculate_calorie_goal(maintenance_calories, validated_data['goal'])
        user = self.context.get('user')
        profile = Profile.objects.create(
            user=user,
            gender=validated_data['gender'],
            weight_lbs=validated_data['weight_lbs'],
            height_cm=validated_data['height_cm'],
            age=validated_data['age'],
            goal=validated_data['goal'],
            activity_level=validated_data['activity_level'],
            maintenance_calories=maintenance_calories,
            calorie_target=calorie_target
        )
        profile.save()
        return profile
        

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['gender', 'weight_lbs', 'height_cm', 'age', 'goal', 'activity_level', 'maintenance_calories', 'calorie_target']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.maintenance_calories = calculate_maintenance_calories(
            instance.weight_lbs,
            instance.height_cm,
            instance.age,
            instance.gender,
            instance.activity_level
        )

        instance.calorie_target = calculate_calorie_goal(
            instance.maintenance_calories,
            instance.goal
        )

        instance.save()
        return instance
