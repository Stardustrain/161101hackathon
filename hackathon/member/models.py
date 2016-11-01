from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin


class ServiceUserManager(BaseUserManager):
    def create_user(self,
                    user_info):

        user = self.model(email=user_info['email'],
                          last_name=user_info['last_name'],
                          first_name=user_info['first_name'],
                          facebook_id=user_info['id'])
        if user.email=='arcanelux@gmail.com':
            user.is_teacher=True
        user.save()
        return user

    def create_superuser(self,
                         email,
                         last_name,
                         first_name,
                         password):
        user = self.model(email=email,
                          last_name=last_name,
                          first_name=first_name
                          )
        user.set_password(password)
        user.is_staff=True
        user.is_superuser=True
        user.save()
        return user


class ServiceUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    facebook_id = models.CharField(max_length=30)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    joined_date = models.DateTimeField(auto_now_add=True)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = ('email')
    REQUIRED_FIELDS = ('first_name','last_name')

    objects = ServiceUserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.first_name







