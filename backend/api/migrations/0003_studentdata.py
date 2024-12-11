# Generated by Django 4.2.5 on 2024-11-18 19:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_question_knowledgelog'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_name', models.CharField(max_length=255)),
                ('is_correct', models.BooleanField(default=False)),
                ('attempts', models.PositiveIntegerField(default=1)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_attempts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Student Attempt',
                'verbose_name_plural': 'Student Attempts',
                'indexes': [models.Index(fields=['student', 'activity_name'], name='api_student_student_4963dd_idx')],
            },
        ),
    ]