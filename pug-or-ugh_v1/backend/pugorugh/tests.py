import json

from os import path
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import (APITestCase,
                                 APIRequestFactory, force_authenticate)

from . import models
from . import serializers
from . import views


# Create your tests here.


class PugOrUghUserTests(APITestCase):
    def setUp(self):
        PROJ_DIR = path.dirname(path.dirname(path.abspath(__file__)))
        filepath = path.join(PROJ_DIR, 'pugorugh', 'static',
                             'dog_details.json')
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            serializer = serializers.DogSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
        self.factory = APIRequestFactory()        
        self.user = models.User.objects.create_superuser(
            'testAdmin', 'ad@min.com', 'adminpassword')
        self.user_pref = models.UserPref.objects.create(user=self.user, gender='m', age=2, size='sml')
        
    def test_register_new_user(self):
        """
        This test posts new user sign in data to create a new user.
        """
        view = views.UserRegisterView.as_view()
        request = self.factory.post('/api/user/login/',
                                    {'username': 'adminTest',
                                     'password': 'admin123'})
        user = views.User.objects.all().first()
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.User.objects.count(), 2)
        self.assertEqual(models.User.objects.get(pk=2).username, 'adminTest')
        
    def test_get_user_pref(self):
        """
        This test checks to see if user preferences can be grabbed from         a GET request using user sign in data.
        """

        request = self.factory.get(reverse('user-pref'))
        force_authenticate(request, user=self.user)

        view = views.CreateUpdateViewUserPref.as_view()
        response = view(request)

        serializer = serializers.UserPrefSerializer(self.user_pref)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        
    def test_post_user_pref(self):
        """
        This test checks to see if new user preferences are posted using         new user preference data.
        """

        new_user_pref_data = {
            'gender': 'm',
            'age': 24,
            'size': 'xl',
        }

        request = self.factory.put(reverse('register-user'), new_user_pref_data)
        force_authenticate(request, user=self.user)

        view = views.CreateUpdateViewUserPref.as_view()
        response = view(request)

        serializer = serializers.UserPrefSerializer(models.UserPref.objects.get())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        
class PugOrUghDogTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = models.User.objects.create(username='test', password='test')
        self.dog = models.Dog.objects.create(
            name='Muffin',
            image_filename='3.jpg',
            breed='Boxer',
            age=24,
            gender='f',
            size='xl'
        )
        self.user_dog = models.UserDog.objects.create(
            user=self.user,
            dog=self.dog,
            status='l'
        )

        
    def test_dog_list(self):
        """ Test getting the full list of current dog objects. """
        

        models.Dog.objects.create(
            name='Lukus',
            image_filename='1.jpg',
            breed='Labrador',
            age=21,
            gender='m',
            size='l'
        )

        request = self.factory.get(reverse('ListDogs'))
        force_authenticate(request, user=self.user)

        view = views.ListDogsView.as_view()
        response = view(request)

        serializer = serializers.DogSerializer(models.Dog.objects.all(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        
    def test_dog_status_list(self):
        """ Test getting specific dogs within a certain status. """

        dog = models.Dog.objects.create(
            name='Dawn',
            image_filename='1.jpg',
            breed='Labrador',
            age=47,
            gender='f',
            size='m'
        )
        
        self.user_dog = models.UserDog.objects.create(
            user=self.user,
            dog=dog,
            status='l'
        )

        request = self.factory.get(reverse('ListDogsStatus', kwargs={'status': 'liked'}))
        force_authenticate(request, user=self.user)

        view = views.ListDogsStatusView.as_view()
        response = view(request, status='liked')

        serializer = serializers.DogSerializer(
            models.Dog.objects.filter(userdog__status='l'), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        
    def test_next_dog(self):
        """ Test getting the next dog by using a dog's pk. """
        

        dog = models.Dog.objects.create(
            name='Phillip',
            image_filename='1.jpg',
            breed='Labrador',
            age=49,
            gender='m',
            size='l'
        )
        
        self.user_dog = models.UserDog.objects.create(
            user=self.user,
            dog=dog,
            status='l'
        )

        request = self.factory.get(reverse('NextDog', kwargs={'status': 'liked',
                                                              'pk': 1}))
        force_authenticate(request, user=self.user)

        view = views.NextDogView.as_view()
        response = view(request, pk=1, status='liked')

        serializer = serializers.DogSerializer(dog)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        


    

