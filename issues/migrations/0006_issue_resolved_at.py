# Generated by Django 4.2.22 on 2025-06-14 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0005_issue_is_resolved'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='resolved_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
