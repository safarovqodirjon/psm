# Generated by Django 4.2.1 on 2023-05-25 07:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("management", "0007_alter_manager_employees_alter_manager_projects_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="project_status",
            field=models.CharField(
                choices=[
                    ("not_started", "Не начат"),
                    ("in_progress", "В процессе"),
                    ("completed", "Завершен"),
                ],
                default="not_started",
                max_length=20,
                verbose_name="Статус проекта",
            ),
        ),
    ]
