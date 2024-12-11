# Generated by Django 4.2.5 on 2024-11-24 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_question_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='images',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='labels',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='options',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]