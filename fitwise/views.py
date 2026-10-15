from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework import authentication,permissions
from rest_framework.response import Response

from fitwise.serializers import UserSerializers,FoodLogSerializer
from fitwise.models import FoodLog
from fitwise.permissions import IsOwner
from fitwise.ai_service import get_diet_plan

from datetime import datetime



class SignUpView(APIView):

    def post(self,request):

        form_data = request.data

        serializer_instance = UserSerializers(data =form_data)

        if serializer_instance.is_valid():

            cleaned_data = serializer_instance.validated_data

            instance = User.objects.create_user(**cleaned_data)

            serializer_instance = UserSerializers(instance)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.error)


class GetMeView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        auth_user = request.user

        instance = User.objects.get(username = auth_user)

        serializer_instance= UserSerializers(instance)

        return Response(data=serializer_instance.data)

class FoodLogListCreate(APIView):

    authentication_classes =[ authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        instance = FoodLog.objects.filter(owner= request.user)

        serializer_instance = FoodLogSerializer(instance,many=True)

        return Response(data=serializer_instance.data)

    def post(self,request):

        form_data = request.data 

        serializer_instance = FoodLogSerializer(data= form_data)

        if serializer_instance.is_valid():

            serializer_instance.save(owner = request.user)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)


class FoodLogRetrieveUpdateDeleteView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[IsOwner]

    def get(self,request,pk=None):

        instance = get_object_or_404(FoodLog,id=pk)

        self.check_object_permissions(request,instance)

        serializer_instance = FoodLogSerializer(instance)

        return Response(data=serializer_instance.data)

    def put(self,request,pk=None):

        instance=get_object_or_404(FoodLog,id=pk)

        self.check_object_permissions(request,instance)

        form_data= request.data

        serialier_instance = FoodLogSerializer(data=form_data,instance=instance)

        if serialier_instance.is_valid():

            serialier_instance.save()

            return Response(data= serialier_instance.data)

        else:

            return Response(data= serialier_instance.errors)

    def delete(self,request,pk=None):

        instance = get_object_or_404(FoodLog,id=pk)

        self.check_object_permissions(request,instance)

        instance.delete()

        return Response(data={"message": "FoodLog deleted"})

class FoodLogSummaryView(APIView):

    authentication_classes =[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        response_data={"todays_total_calorie":0}

        curr_date = datetime.now().date()

        curr_month = datetime.now().month

        curr_year = datetime.now().year

        #======todays total calorie==========

        todays_foodlog= FoodLog.objects.filter(owner=request.user,created_at__date = curr_date)

        if todays_foodlog:

            today_total_calories = todays_foodlog.values("calorie").aggregate(total = Sum("calorie")).get("total")

            response_data["todays_total_calorie"] = today_total_calories

            #categorize calories based on meal_type

            category_calories = todays_foodlog.values("meal_type").annotate(total = Sum("calorie"))

            response_data["meal_type_calorie"] = category_calories

    #===========monthly total Calorie========

        monthly_foodlogs = FoodLog.objects.filter(owner=request.user,created_at__month = curr_month,created_at__year=curr_year)

        if monthly_foodlogs:

            monthly_calories = monthly_foodlogs.values("calorie").aggregate(total = Sum("calorie")).get("total")

            monthly_category_calories = monthly_foodlogs.values("meal_type").annotate(total=Sum("calorie"))

            response_data["monthly_calories"] = monthly_calories
            
            response_data["monthly_meal_type_calories"] = monthly_category_calories

        return Response(data = response_data )

class DietPlaanView(APIView):

    authentication_classes =[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        response_data={"monthly_total_calorie":0}
        
        curr_month = datetime.now().month
        
        curr_year = datetime.now().year

        monthly_foodlogs = FoodLog.objects.filter(owner=request.user,created_at__month = curr_month,created_at__year=curr_year)

        if monthly_foodlogs:

            monthly_calories = monthly_foodlogs.values("calorie").aggregate(total = Sum("calorie")).get("total")

            monthly_category_calories = monthly_foodlogs.values("meal_type").annotate(total=Sum("calorie"))

            response_data["monthly_calories"] = monthly_calories
            
            response_data["monthly_meal_type_calories"] = monthly_category_calories

            diet_plan = get_diet_plan(response_data)

            response_data["diet_plan"] = diet_plan

        return Response(data = response_data )
    


        

        

















