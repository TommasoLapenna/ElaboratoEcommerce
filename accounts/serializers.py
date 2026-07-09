from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        # Il campo read-only serve per non fare autoassegnare ruoli di manager
        extra_kwargs = {'role': {'read_only': True}}

    # Check per username duplicati
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    # Sia min_lenght che validate_username ritornano errori 400 non silent

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data.get('email', ''))
        user.role = 'customer'
        user.set_password(validated_data['password'])
        user.save()
        return user