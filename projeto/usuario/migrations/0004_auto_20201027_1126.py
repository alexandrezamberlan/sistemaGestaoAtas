# Generated by Django 3.0.4 on 2020-10-27 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0001_initial'),
        ('usuario', '0003_auto_20201027_1113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='curso',
        ),
        migrations.AddField(
            model_name='usuario',
            name='curso',
            field=models.ManyToManyField(blank=True, null=True, to='curso.Curso', verbose_name='Curso'),
        ),
    ]
