from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserStatus, CheckLog
from .serializers import UserStatusSerializer, CheckLogSerializer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets

class UserStausViewSet(viewsets.ModelViewSet):
    queryset = UserStatus.objects.all()
    serializer_class = UserStatusSerializer

class CheckLogViewSet(viewsets.ModelViewSet):
    queryset = CheckLog.objects.all()
    serializer_class = CheckLogSerializer


# Create your views here.

# def user_list(request):
#     if request.method =='GET':
#         queryset = User.objects.all()
#         serializer = UserStatusSerializer(queryset)
#         return JsonResponse(serializer.data, safe=False)

    #if request.method =='POST':
