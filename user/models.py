from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserType(models.Model):

    """UserType model for roles."""

    name = models.CharField(max_length=128)

    class Meta:
        db_table = "user_types"

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("must have an email")
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, null=True)
    company_email = models.EmailField(max_length=128, unique=True, null=True)
    user_type = models.ForeignKey("UserType", on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey("Company", on_delete=models.SET_NULL, null=True)
    career_interest = models.ForeignKey("CareerInterest", on_delete=models.SET_NULL, null=True)
    mobile = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    join_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email


class CareerInterest(models.Model):
    career = models.CharField(max_length=128)

    class Meta:
        db_table = "careers"

    def __str__(self):
        return self.career


class Company(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        db_table = "companies"

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        db_table = "departments"

    def __str__(self):
        return self.name
