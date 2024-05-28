# Generated by Django 5.0.6 on 2024-05-25 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all', '0003_remove_assignment_course_remove_assignment_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='connect',
            name='status',
            field=models.CharField(choices=[('teacher', 'Teacher'), ('student', 'Student')], default=1, max_length=10, verbose_name='status:'),
            preserve_default=False,
        ),
    ]
