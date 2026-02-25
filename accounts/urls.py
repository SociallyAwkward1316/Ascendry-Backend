from django.urls import path
from .views import CustomTokenObtainPairView, CustomRefreshTokenView, User_Register, User_Logout, Create_Profile,  Profile_data

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view()),
    path('refresh/', CustomRefreshTokenView.as_view()),
    path('register/', User_Register),
    path('logout/', User_Logout),
    path('create_profile/', Create_Profile),
    path('profile/', Profile_data),

]