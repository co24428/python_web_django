# Generated by Django 2.2.5 on 2020-01-07 03:51

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Table2',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('kor', models.IntegerField(null=True)),
                ('eng', models.IntegerField(null=True)),
                ('math', models.IntegerField(null=True)),
                ('classroom', models.CharField(max_length=3)),
                ('regdate', models.DateField(auto_now_add=True)),
            ],
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
