# Generated by Django 2.2.10 on 2020-02-26 13:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_premises_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='opexitem',
            options={'verbose_name': 'Opex item', 'verbose_name_plural': 'Opex items'},
        ),
        migrations.AddField(
            model_name='opexitem',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opexitem',
            name='default',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='opexitem',
            name='deleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='opexitem',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='opexitem',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='opex_items', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opexitem',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='opexitem',
            name='fullname',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
