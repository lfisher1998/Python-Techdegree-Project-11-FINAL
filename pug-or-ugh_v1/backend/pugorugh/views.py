from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView,
                                     RetrieveUpdateAPIView, DestroyAPIView)
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status as api_status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.db.models import Q
from django.contrib.auth.models import User

from . import models
from . import serializers

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'dogs': reverse('ListDogs', request=request, format=format)
    })

class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer
    
#/api/user/preferences/    
class CreateUpdateViewUserPref(RetrieveUpdateAPIView, CreateModelMixin):
    """Create, update, or view user preferences."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    lookup_field = None
    
    
    def get_object(self):
        try:
            user_pref = models.UserPref.objects.get(user=self.request.user.id)
            
        except models.UserPref.DoesNotExist:
            user_pref = models.UserPref.objects.create(user=self.request.user)
            
            
        return user_pref
        

    

#/api/dog/<pk>/<status>/    
class UpdateStatus(APIView):
    """ This view updates a dog's status to liked or disliked. """ 
    
    def put(self, request, pk, status, format=None):
        status_choice = None
        
        for choice in models.UserDog.STATUS_CHOICES:
            if choice[1].lower() == status:
                status_choice = choice[0]
        
        serializer = serializers.UserDogSerializer(
            data={'user': self.request.user.id, 'dog': pk, 'status': status_choice})
        if serializer.is_valid():
            try:
                user_dog = models.UserDog.objects.get(user=self.request.user.id, dog=pk)
                user_dog.status = status_choice
            except models.UserDog.DoesNotExist:
                user_dog = models.UserDog.objects.create(**serializer.validated_data)
            user_dog.save()
            
            return Response(serializer.data, status=api_status.HTTP_200_OK)
        return Response(serializer.errors, status=api_status.HTTP_400_BAD_REQUEST)
    
# /api/dog/(?P<pk>-?\d+)/(?P<status>[\w\-]+)/next/
class NextDogView(RetrieveAPIView, CreateModelMixin):
    """ This view gets you the next dog associated with its status. """
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    serializer_class = serializers.DogSerializer
    queryset = models.Dog.objects.all()
    
    @property
    def given_status(self):
        status = None
        
        try:
            give_status = self.kwargs.get('status').lower()
        except AttributeError:
            raise ValidationError(
                'Status was incorrect. Must be liked, disliked, or undecided.')
        else:
            if give_status not in ['liked', 'disliked', 'undecided']:
                raise ValidationError(
                    'Status was incorrect. Must be liked, disliked, or undecided.'
                )
        for choice in models.UserDog.STATUS_CHOICES:
            if choice[1].lower() == give_status:
                status = choice[0]

        return status

    def get_queryset(self):
        """Return a queryset based on dog pk and the user dog's status."""

        if not self.given_status:

            user_pref = self.request.user.userpref_set.get()

            available_dogs = self.queryset.filter(
                gender__in=user_pref.gender.split(","),
                size__in=user_pref.size.split(","),
                age__in=user_pref.ages_int_range,
            )
            
        else:
            available_dogs = self.queryset

        return available_dogs.filter(
            userdog__status=self.given_status,
            userdog__user__id=self.request.user.id, 
            id__gt=self.kwargs.get('pk')
        )
    
    def get_object(self):
        """Find the first dog in the queryset or give a 404 if there is none"""

        queryset = self.get_queryset()
        
        
        if len(queryset) == 1:
            dog = queryset[0]
        else:
            dog = self.get_queryset().first()
            
        if not dog:
            dogs = models.Dog.objects.all()
            for dog in dogs:
                dog = models.UserDog.objects.create(
                    user=self.request.user,
                    dog=dog,
                    status=None
                )
            
        

        

        return dog
    
# /api/dog/<pk>/undecided/
class UpdateUndecided(DestroyAPIView):
    """ This view deletes a dog's status. """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.DogSerializer
    queryset = models.Dog.objects.all()    

# /api/dogs/
class ListDogsView(ListCreateAPIView):
    """ This view lists all dog objects """
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    serializer_class = serializers.DogSerializer
    queryset = models.Dog.objects.all()

#/api/dogs/(?P<status>[\w\-]+)/
class ListDogsStatusView(ListAPIView):
    """ This view displays all dogs based on a liked,
    disliked, undecided filter 
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    serializer_class = serializers.DogSerializer
    queryset = models.Dog.objects.all()
    
    @property
    def given_status(self):
        status = None
        
        try:
            give_status = self.kwargs.get('status').lower()
        except AttributeError:
            raise ValidationError(
                'Status was incorrect. Must be liked, disliked, or undecided.')
        else:
            if give_status not in ['liked', 'disliked', 'undecided']:
                raise ValidationError(
                    'Status was incorrect. Must be liked, disliked, or undecided.'
                )
        for choice in models.UserDog.STATUS_CHOICES:
            if choice[1].lower() == give_status:
                status = choice[0]

        return status

    
    def get_queryset(self):
        """Return a queryset based on dog pk and the user dog's status."""
        
        return self.queryset.filter(
            Q(userdog__status=self.given_status) &
            Q(userdog__user__id=self.request.user.id) 
        )


    
    
        