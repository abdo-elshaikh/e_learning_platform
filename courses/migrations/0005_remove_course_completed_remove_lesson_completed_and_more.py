# Generated by Django 5.1.4 on 2024-12-30 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_rename_is_complete_course_completed_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='completed',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='completed',
        ),
        migrations.AddField(
            model_name='enrollment',
            name='completed_lessons',
            field=models.ManyToManyField(blank=True, to='courses.lesson'),
        ),
    ]
