from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
User = get_user_model()
class RgisterSeriallizer(serializers.ModelSerializer):
    password2=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=["first_name","phone_number","password","password2"]
        extra_kwargs={
            "password":{"write_only":True}
        }
    def save(self):
        password=self.validated_data["password"]
        password2=self.validated_data["password2"]
        if password!=password2:
            raise serializers.ValidationError({"error":"P1 and P2 should be the same"})
        if User.objects.filter(phone_number=self.validated_data["phone_number"]).exists():
            raise serializers.ValidationError({"error":"Phone number already exists"})
        if User.objects.filter(first_name=self.validated_data["first_name"]).exists():
            raise serializers.ValidationError({"error":"User name already exists"})
        account=User(phone_number=self.validated_data["phone_number"],first_name=self.validated_data["first_name"])
        account.set_password(password)
        account.save()
        return account

class LoginSerializer(serializers.Serializer):

    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def save(self):
        phone_number = self.validated_data["phone_number"]
        password = self.validated_data["password"]

        user = authenticate(
            phone_number=phone_number,
            password=password
        )

        if user is None:
            raise serializers.ValidationError({
                "error": "Invalid phone number or password"
            })

        if not user.is_active:
            raise serializers.ValidationError({
                "error": "Account is inactive"
            })
        return user