from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            from django.contrib.auth.models import User
            user = User.objects.get(email=credentials["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with given email and password does not exists"
            )

        if not user.check_password(credentials["password"]):
            raise serializers.ValidationError("Invalid password")
        data = {}
        refresh = self.get_token(user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data
