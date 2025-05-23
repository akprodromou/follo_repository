# Generated by Django 3.1.3 on 2021-01-29 06:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectcategory_number', models.IntegerField(unique=True)),
                ('projectcategory_name', models.CharField(max_length=264, unique=True)),
                ('projectcategory_name_html', models.TextField(blank=True, default='', editable=False)),
            ],
            options={
                'ordering': ['projectcategory_number'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_number', models.IntegerField(unique=True)),
                ('project_name', models.CharField(max_length=264, unique=True)),
                ('project_stage', models.CharField(choices=[('Concept Design', 'CD - Concept Design'), ('Schematic Design', 'SD - Schematic Design'), ('Design Development', 'DD - Design Development'), ('Issued for Construction', 'IFC - Issued for Construction'), ('Closed', 'Closed')], default='CD', max_length=30)),
                ('project_delivery_date', models.DateField()),
                ('project_status', models.CharField(choices=[('On time', 'On time'), ('Delayed', 'Delayed')], default='On time', max_length=30)),
                ('project_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_projects', to='projects.projectcategory')),
                ('project_creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_creator', to=settings.AUTH_USER_MODEL)),
                ('project_members', models.ManyToManyField(related_name='user_member_projects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['project_number'],
                'unique_together': {('project_number', 'project_creator')},
            },
        ),
    ]
