# Generated by Django 4.2.5 on 2024-11-24 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_question_id_question_labels_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.JSONField(default=dict),
        ),
    ]