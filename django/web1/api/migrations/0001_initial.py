# Generated by Django 2.2.5 on 2020-01-10 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('price', models.IntegerField(null=True)),
                ('regdate', models.DateField(auto_now_add=True)),
            ],
        ),
    ]