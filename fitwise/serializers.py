from django.contrib.auth.models import User
from rest_framework import serializers
from fitwise.models import FoodLog

class UserSerializers(serializers.ModelSerializer):

    class Meta:

        model= User

        fields = ["username","email","password"]

        read_only_fields = ["id"]


class FoodLogSerializer(serializers.ModelSerializer):


    class Meta:

        model = FoodLog

        fields = "__all__"

        read_only_fields = ["id","owner","created_at","updated_at"]