# Generated by Django 5.1.7 on 2025-04-02 13:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0002_remove_proyecto_user_proyecto_estado_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='asignados',
            field=models.ManyToManyField(default=None, related_name='asignaciones', to=settings.AUTH_USER_MODEL),
        ),
    ]
