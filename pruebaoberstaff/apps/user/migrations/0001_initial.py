# Generated by Django 5.1.7 on 2025-03-28 23:38

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('pk_publica', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Creado', models.DateTimeField(auto_now_add=True)),
                ('Modificado', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('Status', models.BooleanField(default=True)),
                ('Nombre_completo', models.CharField(default='', max_length=60)),
                ('Nombres', models.CharField(default='', max_length=50)),
                ('Apellidos', models.CharField(default='', max_length=50)),
                ('Contacto', models.CharField(default='', max_length=50)),
                ('Comentarios', models.CharField(default='', max_length=200)),
                ('Codigo', models.CharField(blank=True, max_length=60, null=True)),
                ('validacion_lvl1_telefono', models.BooleanField(default=False)),
                ('validacion_lvl2_email', models.BooleanField(default=False)),
                ('lat', models.CharField(blank=True, max_length=60, null=True)),
                ('log', models.CharField(blank=True, max_length=60, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Creado', models.DateTimeField(auto_now_add=True)),
                ('Modificado', models.DateTimeField(auto_now=True)),
                ('Status', models.BooleanField(default=True)),
                ('pk_publica', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Codigo', models.CharField(blank=True, max_length=60, null=True)),
                ('Nombre', models.CharField(max_length=15)),
                ('avatars', models.BooleanField(default=False)),
                ('centro_inteligencia', models.BooleanField(default=False)),
                ('social_listening', models.BooleanField(default=False)),
                ('ai_listening', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='userPartial',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('migracion', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('user.user',),
        ),
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Creado', models.DateTimeField(auto_now_add=True)),
                ('Modificado', models.DateTimeField(auto_now=True)),
                ('Status', models.BooleanField(default=True)),
                ('pk_publica', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Codigo', models.CharField(blank=True, max_length=60, null=True)),
                ('Nombres', models.CharField(default='', max_length=50)),
                ('Apellidos', models.CharField(default='', max_length=50)),
                ('Telefono', models.CharField(default='', max_length=50)),
                ('Correo', models.CharField(default='', max_length=50)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contactosuser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='keysRecovery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Creado', models.DateTimeField(auto_now_add=True)),
                ('Modificado', models.DateTimeField(auto_now=True)),
                ('Status', models.BooleanField(default=True)),
                ('pk_publica', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Codigo', models.CharField(blank=True, max_length=60, null=True)),
                ('keysRecovery', models.CharField(blank=True, max_length=15, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='keysRecovery', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='user',
            name='rol',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roluser', to='user.rol'),
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Creado', models.DateTimeField(auto_now_add=True)),
                ('Modificado', models.DateTimeField(auto_now=True)),
                ('Status', models.BooleanField(default=True)),
                ('pk_publica', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Codigo', models.CharField(blank=True, max_length=60, null=True)),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Token', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
