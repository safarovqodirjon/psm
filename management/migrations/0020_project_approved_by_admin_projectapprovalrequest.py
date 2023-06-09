# Generated by Django 4.2.1 on 2023-05-28 03:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("management", "0019_delete_projectapprovalrequest"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="approved_by_admin",
            field=models.BooleanField(
                default=False, verbose_name="Одобрено администратором"
            ),
        ),
        migrations.CreateModel(
            name="ProjectApprovalRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "request_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата запроса"
                    ),
                ),
                (
                    "manager",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="approval_requests",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Менеджер",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="approval_requests",
                        to="management.project",
                        verbose_name="Проект",
                    ),
                ),
            ],
            options={
                "verbose_name": "Запрос на одобрение проекта",
                "verbose_name_plural": "Запросы на одобрение проекта",
            },
        ),
    ]
