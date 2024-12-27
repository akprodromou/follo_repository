# Generated by Django 3.1.3 on 2021-01-29 06:03

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_description', models.CharField(max_length=264)),
                ('task_description_html', models.TextField(editable=False)),
                ('task_status', models.CharField(choices=[('Completed', 'Completed'), ('Pending', 'Pending')], default='Pending', max_length=30)),
                ('task_creation_date', models.DateTimeField(auto_now=True)),
                ('task_due_date', models.DateField()),
                ('task_completion_date', models.DateTimeField(blank=True, null=True)),
                ('task_asignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Assign task to')),
                ('task_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tasks', to=settings.AUTH_USER_MODEL)),
                ('task_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_tasks', to='projects.project')),
            ],
            options={
                'ordering': ['task_due_date'],
            },
        ),
        migrations.CreateModel(
            name='Worktime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worktime_date', models.DateField(default=datetime.date.today)),
                ('worktime_hour', models.FloatField(verbose_name='Hours')),
                ('worktime_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_time', to='team.task')),
                ('worktime_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_time', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-worktime_date'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userprofile_photo', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('userprofile_position', models.CharField(max_length=20)),
                ('userprofile_projects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_projects', to='projects.project')),
                ('userprofile_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField()),
                ('comment_created_date', models.DateTimeField(auto_now=True)),
                ('comment_viewed', models.BooleanField(default=False)),
                ('comment_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_comment', to='team.task')),
            ],
            options={
                'ordering': ['comment_created_date'],
            },
        ),
    ]
