# Generated by Django 4.2.5 on 2024-11-15 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0002_remove_customuser_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='ai_assistant',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
