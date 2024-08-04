# Generated by Django 4.2.13 on 2024-08-03 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0002_alter_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='calificaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tarea', models.CharField(max_length=80)),
                ('nota', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_entrega', models.DateField(blank=True, null=True)),
                ('comentario', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Calificaciones',
            },
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
    ]