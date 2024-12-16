# Generated by Django 4.2 on 2024-12-16 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foring', '0006_alter_comment_task_alter_task_priority_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(blank=True, choices=[('1', 'To Do'), ('2', 'In Progress'), ('3', 'Done')], max_length=50, null=True),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]