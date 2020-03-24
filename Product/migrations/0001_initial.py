# Generated by Django 2.2.7 on 2020-02-13 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('productcategory_id', models.AutoField(primary_key=True, serialize=False)),
                ('productcategory_name', models.CharField(max_length=36)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSubcategory',
            fields=[
                ('productsubcategory_id', models.AutoField(primary_key=True, serialize=False)),
                ('productsubcategory_name', models.CharField(max_length=36)),
                ('productcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.ProductCategory')),
            ],
        ),
        migrations.CreateModel(
            name='ProductInformation',
            fields=[
                ('productinformation_id', models.AutoField(primary_key=True, serialize=False)),
                ('productinformation_name', models.CharField(max_length=36)),
                ('productinformation_details', models.TextField()),
                ('product_verify', models.BooleanField(default=False)),
                ('productinformation_baseprice', models.FloatField()),
                ('productcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.ProductCategory')),
                ('productsubcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.ProductSubcategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.User')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('productimages_id', models.AutoField(primary_key=True, serialize=False)),
                ('productimages_image', models.FileField(upload_to='product/')),
                ('productinformation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.ProductInformation')),
            ],
        ),
    ]
