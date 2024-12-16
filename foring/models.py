from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=email,
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Project(models.Model):
    name        = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    owner       = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class ProjectMember(models.Model):
    USER_ROLE = {
        ('1', 'Admin'),
        ('2', 'Member'),
    }
    project    = models.ForeignKey(Project, on_delete=models.CASCADE)
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    role       = models.CharField(max_length=50, choices=USER_ROLE)

    def __str__(self):
        return f"{self.user.username} - {self.role} in {self.project.name}"
    

class Task(models.Model):
    STATUS_CHOICES = { 
        ('1', 'To Do'),
        ('2', 'In Progress'),
        ('3', 'Done')
    }

    PRIORITY_CHOICES = { 
        ('1', 'Low'),
        ('2', 'Medium'),
        ('3', 'High')
    }
    title       = models.CharField(max_length=255)
    tescription = models.TextField(blank=True, null=True)
    status      = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True, blank=True)
    priority    = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='Medium')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    project     = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    due_date    = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content     = models.TextField()
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    task        = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.title}"