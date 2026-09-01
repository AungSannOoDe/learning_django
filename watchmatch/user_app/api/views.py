from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from user_app.api.serializers import RgisterSeriallizer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user

    data = {
        "id": user.id,
        "name": user.first_name,
        "phone_number": user.phone_number,
    }

    return Response(data)
@api_view(['POST',])
def logout_view(request):
    if request.method=="POST":
        request.user.auth_token.delete()
        data={"message":"User logout successfully"}
        return Response(data,status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([AllowAny])
def registration_view(request):

    serializer = RgisterSeriallizer(data=request.data)
    if serializer.is_valid():
        account=serializer.save()
        token, created = Token.objects.get_or_create(user=account)
        data = {
            "token": token.key,
            "user": serializer.data,
            "message": "Register created successfully",
        }
        return Response(
            data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )