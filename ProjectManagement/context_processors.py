from django.contrib.auth import get_user_model
from django.http import JsonResponse
User = get_user_model()

def user_colors(request):
    if request.user.is_authenticated:
        R_name_length = len(str(request.user))*40%255
        G_date_joined = int(str(request.user.date_joined)[14:16])*40%255
        B_date_joined = int(str(request.user.date_joined)[17:19])*40%255
    else:
        R_name_length = 0
        G_date_joined = 0
        B_date_joined = 0
    return {
        'R_name_length': R_name_length,
        'G_date_joined': G_date_joined,
        'B_date_joined': B_date_joined,
    }
