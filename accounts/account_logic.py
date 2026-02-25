def calculate_maintenance_calories(weight_lbs, height_cm, age, gender, activity_level):
    if gender == "male":
        bmr = (10 * (weight_lbs * 0.45359237)) + (6.25 * height_cm) - (5 * age) + 5
    elif gender == "female":
        bmr = (10 * (weight_lbs * 0.45359237)) + (6.25 * height_cm) - (5 * age) - 161

    if activity_level == "sedentary":
        activity = 1.2
    elif activity_level == "light":
        activity = 1.375
    elif activity_level == "active":
        activity = 1.725
    return int(bmr * activity)

def calculate_calorie_goal(maintenance_calories, goal):
    if goal == "bulk":
        goal_calories =  maintenance_calories + 300
    elif goal == "cut":
        goal_calories = maintenance_calories - 300
    elif goal == "maintain":
        goal_calories  = maintenance_calories
    
    return goal_calories