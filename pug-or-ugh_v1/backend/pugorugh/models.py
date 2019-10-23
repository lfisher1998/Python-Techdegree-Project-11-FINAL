from django.db import models
from django.db import IntegrityError

from django.contrib.auth.models import User


DOG_AGES = {
    'b': range(0, 7),
    'y': range(7, 13),
    'a': range(13, 85),
    's': range(85, 361),
}


class Dog(models.Model):
    """ This model involves a dog in the app """
    GENDER_CHOICES = (
        ('m', 'male'),
        ('f', 'female'),
        ('u', 'unknown'),
    )
    SIZE_CHOICES = (
        ('s', 'small'),
        ('m', 'medium'),
        ('l', 'large'),
        ('xl', 'extra large'),
        ('u', 'unknown'),
    )
    
    
    
    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField(max_length=255, blank=True, default="")
    
    # age is integer for months
    age = models.IntegerField()
    
    # 'm' for male, 'f' for female, 'u' for unknown
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES
    )
    
    # 's' for small, 'm' for medium, 'l' for large, 'xl' for extra large,
    # 'u' for unknown
    size = models.CharField(
        max_length=255,
        choices=SIZE_CHOICES
    )
    
    @property
    def get_age_stage(self):
        if self.age < 12:
            return 'b'
        elif self.age < 36:
            return 'y'
        elif self.age < 72:
            return 'a'
        else:
            return 's'

    def save(self, *args, **kwarg):
        self.age_stage = self.get_age_stage
        super(Dog, self).save(*args, **kwarg)
    
    def __str__(self):
        return self.name
    
class UserDog(models.Model):
    """ This model connects a user and a dog """
    STATUS_CHOICES = (
        ('l', 'liked'),
        ('d', 'disliked'),
    )
    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    dog = models.ForeignKey('Dog', on_delete=models.CASCADE)
    
    # 'l' for liked, 'd' for disliked, 'u' for undecided
    status = models.CharField(
        max_length=1,
        choices = STATUS_CHOICES,
        null=True,
    )
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            user_dog = UserDog.objects.filter(user=self.user, dog=self.dog)
            if user_dog.count() != 0:
                raise IntegrityError(
                    "UserDog item with same dog field exist on user_dog %r" % user_dog[0].pk)
        super(UserDog, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.user.username
    
class UserPref(models.Model):
    """ This model includes user preferences """
    
    GENDER_CHOICES = (
        ('m', 'male'),
        ('f', 'female'),
        ('u', 'unknown'),
    )
    SIZE_CHOICES = (
        ('s', 'small'),
        ('m', 'medium'),
        ('l', 'large'),
        ('xl', 'extra large'),
        ('u', 'unknown'),
    )
    
    AGE_CHOICES = (
        ('b', 'Baby'),
        ('y', 'Young'),
        ('a', 'Adult'),
        ('s', 'Senior'),
    )
    
    
    user = models.ForeignKey('auth.User',
                            on_delete=models.CASCADE)
    
    
    gender = models.CharField(max_length=15)
    age = models.CharField(max_length=15)
    size = models.CharField(max_length=15)
    
    @property
    def ages_int_range(self):
        """Takes an age given and translates it to a year range"""

        ages = []
        for age_reference, age_range in DOG_AGES.items():
            if age_reference in self.age:
                ages.extend(age_range)

        return ages
    
    def __str__(self):
        return self.user.username
    
