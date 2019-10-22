from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = '__all__'


class DogSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        dog = models.Dog.objects.create(
            name=validated_data['name'],
            age=validated_data['age'],
            gender=validated_data['gender'],
            image_filename=validated_data['image_filename'],
            size=validated_data['size'],
        )
        return dog
        try:
            dog = models.Dog.objects.filter(
                name=validated_data['name']).update(
                breed=validated_data['breed'],
            )
        except KeyError:
            pass
        
    
    class Meta:
        model = models.Dog
        fields = (
            '__all__'
        )
        
        
class UserDogSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserDog
        fields = (
            'id',
            'dog',
            'status',
            'user',
        )
        extra_kwargs = {'user': {'write_only': True}}
        
class UserPrefSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.UserPref
        fields = (
            'id',
            'gender',
            'age',
            'size',
        )
