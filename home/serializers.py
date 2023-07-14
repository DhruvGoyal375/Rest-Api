from rest_framework import serializers
from .models import Person, Color
from django.contrib.auth.models import User


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']


class PeopleSerializer(serializers.ModelSerializer):
    color = ColorSerializer()  # don't use it with post method
    color_info = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = "__all__"

    def get_color_info(self, obj):   # use the name of SerializerMethodField after get_
        if obj.color:
            color_obj = Color.objects.get(id=obj.color.id)
            return {'color_name': color_obj.color_name, "hexcode": "#1111"}

    def validate(self, data):
        special_characters = "!@#$%^&*()_+<>?:.,;][}{|"

        if any(c in special_characters for c in data['name']):
            raise serializers.ValidationError(
                "Name must not contain special characters")

        if data.get("age") and data['age'] < 18:
            raise serializers.ValidationError("Age must be greater than 18")
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    # email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=100)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=100)
    # confirm_password = serializers.CharField(max_length=100)

    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         raise serializers.ValidationError(
    #             "Password and confirm password must be same")
    #     return data

    def validate(self, data):
        if data["username"]:
            if User.objects.filter(username=data["username"]).exists():
                raise serializers.ValidationError(
                    "Username already exists")
            if User.objects.filter(email=data["email"]).exists():
                raise serializers.ValidationError(
                    "email already taken")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"], email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return validated_data
