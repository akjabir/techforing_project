from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from foring.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/register/', RegisterUserView.as_view(), name='register_user'),
    path('users/login/', LoginUserView.as_view(), name='login_user'),
    path('api/projects/', ProjectListCreateView.as_view(), name='project_list_create'),
    path('api/tasks/<int:task_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('', include('foring.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
