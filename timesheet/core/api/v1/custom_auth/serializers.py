from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from timesheet.core.api.v1.serializers import UserSerializer


class TokenObtainPairSerializerCustom(TokenObtainPairSerializer):
    username_field = "login"

    def validate(self, attrs):
        data_original = super().validate(attrs)
        user = UserSerializer(instance=self.user)

        data = {"token": data_original["access"], "user": user.data}

        return data
