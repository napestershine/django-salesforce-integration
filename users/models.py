from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, about, company, department, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            about=about,
            company=company,
            department=department
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    about = models.TextField(default=None, blank=True, null=True)
    address = models.CharField(max_length=255, default=None, blank=True, null=True)
    company = models.CharField(max_length=255, default=None, blank=True, null=True)
    department = models.CharField(max_length=255, default=None, blank=True, null=True)
    first_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    last_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    username = models.CharField(max_length=255, default=None, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Account(models.Model):
    name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200, default=None, blank=True, null=True)
    description = models.TextField(default=None, blank=True, null=True)
    industry = models.CharField(max_length=200, default=None, blank=True, null=True)
    address = models.CharField(max_length=200, default=None, blank=True, null=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=200, default=None, blank=True, null=True)
    account_id = models.CharField(max_length=200, default=None, blank=True, null=True)
    description = models.TextField(default=None, blank=True, null=True)
    department = models.CharField(max_length=200, default=None, blank=True, null=True)
    address = models.CharField(max_length=200, default=None, blank=True, null=True)
    email = models.EmailField(max_length=200, default=None, blank=True, null=True)
    birthDate = models.DateField(default=None, blank=True, null=True)

    def __str__(self):
        return self.name
