# Generated by Django 4.2.5 on 2024-11-18 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_studentdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentdata',
            name='skill',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]