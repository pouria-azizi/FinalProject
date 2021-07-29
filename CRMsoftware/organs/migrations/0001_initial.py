# Generated by Django 3.2.5 on 2021-07-29 06:53

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=150)),
                ('organization_phone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='phone number invalid', regex='^0[0-9]{2,}[0-9]{7,}$')])),
                ('employees_number', models.CharField(max_length=10000)),
                ('owner', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('owner_phone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='phone number invalid', regex='^0[0-9]{2,}[0-9]{7,}$')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('organization_product', models.ManyToManyField(to='organs.OrganizationProduct')),
            ],
        ),
        migrations.AddConstraint(
            model_name='organization',
            constraint=models.UniqueConstraint(fields=('name', 'created_by'), name='UniqueOrgan'),
        ),
    ]
