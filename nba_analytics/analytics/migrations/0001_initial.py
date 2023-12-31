# Generated by Django 4.2.6 on 2023-10-21 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NBAPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('team', models.CharField(max_length=50)),
                ('points_per_game', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
