# Generated by Django 2.2.10 on 2020-02-26 16:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200226_1312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assetopex',
            old_name='value',
            new_name='montly_value',
        ),
        migrations.RemoveField(
            model_name='assetopex',
            name='fullname',
        ),
        migrations.RemoveField(
            model_name='assetopex',
            name='name',
        ),
        migrations.AddField(
            model_name='assetopex',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assetopex',
            name='deleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='assetopex',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='assetopex',
            name='update',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='assetopex',
            name='vat',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assetopex',
            name='asset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opex', to='api.Asset'),
        ),
    ]
