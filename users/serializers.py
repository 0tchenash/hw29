from rest_framework import serializers
from users.models import User, Location
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from datetime import date

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role']


class UserDetailSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name")

    class Meta:
        model = User
        exclude = ['password']

def EmailValidator(value: str):
    if 'rambler' in value.split('@')[1]:
        raise ValidationError(
            'Invalid email address.',
            params = {'value': value}
        )

class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    location = serializers.SlugRelatedField(
        required=False,
        slug_field='name',
        queryset=Location.objects.all())

    email = serializers.CharField(max_length=50, validators=[UniqueValidator(queryset=User.objects.all()), EmailValidator])

    class Meta:
        model = User
        fields = '__all__'
    
    def is_valid(self, raise_exception=False):
        self._location = self.initial_data.pop('location', None)
        return super().is_valid(raise_exception=raise_exception)
    
    def create(self, validated_data):

        user = super().create(validated_data)
        user.set_password(user.password)
        user.age = date.today().year - user.birth_date.year
        user.save()
        
        if self._location:
            location_obj = Location.objects.get_or_create(name=self._location)[0]
            user.location = location_obj
            user.save()
        
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    location = serializers.SlugRelatedField(
        required=False, 
        slug_field='name', 
        queryset=Location.objects.all())

    class Meta:
        model = User
        exclude = ['id']

    def is_valid(self, raise_exception=False):
        self._location = self.initial_data.pop('location', None)
        return super().is_valid(raise_exception=raise_exception)
    
    def save(self):
        user = super().save()
        if self._location:
            location_obj = Location.objects.get_or_create(name=self._location)[0]
            user.location = location_obj
            user.save()
        return user


class UserDestroySerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id']
