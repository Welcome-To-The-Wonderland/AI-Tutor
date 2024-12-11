from django.db import models
from userauths.models import CustomUser
from django.conf import settings
import uuid
from django.db.models import JSONField


class Thread(models.Model):
    assistant_id = models.CharField(max_length=100)
    question = models.TextField()
    thread_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Thread {self.thread_id} for Assistant {self.assistant_id}"


class StudentData(models.Model):
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='student_attempts'
    )
    activity_name = models.CharField(max_length=255)
    skill = models.CharField(max_length=255, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=1)
    unique_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['student', 'activity_name']),
        ]
        verbose_name = "Student Attempt"
        verbose_name_plural = "Student Attempts"

    def __str__(self):
        return f"Student: {self.student.email}, Activity: {self.activity_name}, Skill: {self.skill}, Correct: {self.is_correct}, Attempts: {self.attempts}"


class Question(models.Model):
    activity = models.CharField(max_length=255, default="Unknown")
    question_type = models.CharField(max_length=255)
    question_text = models.TextField(primary_key=True)
    skill = models.CharField(max_length=255)
    hint = models.TextField(null=True, blank=True)
    answer = models.JSONField(default=dict)
    options = models.JSONField(null=True, blank=True, default=list)
    labels = models.JSONField(null=True, blank=True, default=list)
    images = models.JSONField(null=True, blank=True, default=list)
    center_image = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.activity} - {self.question_text}"
