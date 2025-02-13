# Generated by Django 3.2.4 on 2021-06-18 17:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to=settings.AUTH_USER_MODEL)),
                ('achievements', models.ManyToManyField(db_table='teacher_archivement', related_name='teachers', to='persons.Achievement')),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='persons.personinfo')),
            ],
            options={
                'db_table': 'teacher',
            },
        ),
    ]
