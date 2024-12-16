from django.shortcuts import render
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework import serializers, views, response, status
from rest_framework.permissions import IsAuthenticated
from django.urls import path
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from foring.models import *
from foring.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from rest_framework.decorators import action

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
        user.save(using=self._db)
        return user

class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None, partial=False):
        user = get_object_or_404(User, pk=pk)
        serializer = self.get_serializer(user, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response({'message': 'User deleted'}, status=status.HTTP_204_NO_CONTENT)
        

class ProjectListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        serializer = self.get_serializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, partial=False):
        project = get_object_or_404(Project, pk=pk)
        serializer = self.get_serializer(project, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return Response({'message': 'Project deleted'}, status=status.HTTP_204_NO_CONTENT)

    
class TaskListCreateView(APIView):
    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        data = request.data.copy()
        data['project'] = project.id
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def retrieve(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        serializer = self.get_serializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        serializer = self.get_serializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return Response({"detail": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class CommentListCreateView(APIView):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        comments = Comment.objects.filter(task=task)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        user = request.user 
        
        data = request.data.copy()
        data['task'] = task.id
        data['user'] = user.id
        
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs.get('task_id', None)
        if task_id:
            return Comment.objects.filter(task_id=task_id)
        return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def retrieve(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = self.get_serializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = self.get_serializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = self.get_serializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response({"detail": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)