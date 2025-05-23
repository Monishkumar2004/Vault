from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class CustomUserManager(BaseUserManager):

    # for creating a normal user through registration page
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        extra_fields.setdefault('user_type', 2)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    # for creating operaions user from the terminal
    def create_superuser(self, email, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 1) #forces to ops user

        return self.create_user(email, password, **extra_fields)
    



class CustomUser(AbstractUser):

    email = models.EmailField(unique = True, max_length= 100)

    # specify the field to be used for auth to be email. overriders the username
    USERNAME_FIELD = "email"

    # Additional field required for creating a username
    REQUIRED_FIELDS = ['username'] 

    USER = (
        (1, 'ops_user'),
        (2, 'client'),
    )


    objects = CustomUserManager()


    user_type = models.IntegerField(choices=USER, default=2)

    def __str__(self):
        return self.email

