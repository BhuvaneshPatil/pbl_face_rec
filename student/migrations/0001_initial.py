# Generated by Django 3.2 on 2021-04-23 13:37

from django.db import migrations, models
import student.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('rollNo', models.CharField(max_length=10, unique=True)),
                ('photo', models.ImageField(blank=True, upload_to=student.models.path_and_rename)),
            ],
        ),
    ]