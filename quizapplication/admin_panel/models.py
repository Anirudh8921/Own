from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class AdminUserManager(BaseUserManager):
    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("Superuser must have an email address")
        admin = self.model(email=self.normalize_email(email))
        admin.set_password(password)
        admin.is_superuser = True
        admin.is_staff = True
        admin.save(using=self._db)
        return admin

class AdminUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    objects = AdminUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email
