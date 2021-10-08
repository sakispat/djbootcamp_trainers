# Generated by Django 3.2.4 on 2021-07-19 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('subject', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'trainer',
            },
        ),
    ]