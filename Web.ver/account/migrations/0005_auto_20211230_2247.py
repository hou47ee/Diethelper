# Generated by Django 3.0.7 on 2021-12-30 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0004_auto_20211230_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodydata',
            name='member',
            field=models.ForeignKey(db_column='member', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bodydata',
            name='time',
            field=models.DateTimeField(primary_key=True, serialize=False),
        ),
    ]