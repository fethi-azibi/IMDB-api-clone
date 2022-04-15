from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        # to add specific attribute with
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        if self.validated_data['password'] != self.validated_data['password2']:
            raise serializers.ValidationError({'error': 'passwords are not matching'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'email already exists'})

        account = User.objects.create(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(self.validated_data['password'])
        account.save()
        return account
