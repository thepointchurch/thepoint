# pylint: disable=invalid-name

from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Family",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("name", models.CharField(max_length=30)),
                ("phone_home", models.CharField(max_length=15, verbose_name="Home Phone", null=True, blank=True)),
                ("phone_mobile", models.CharField(max_length=15, verbose_name="Mobile Phone", null=True, blank=True)),
                ("email", models.EmailField(max_length=254, null=True, blank=True)),
                ("street", models.CharField(max_length=128, null=True, blank=True)),
                ("suburb", models.CharField(max_length=32, null=True, blank=True)),
                ("postcode", models.CharField(max_length=6, null=True, blank=True)),
                ("is_current", models.BooleanField(default=True, verbose_name="Current")),
                ("anniversary", models.DateField(null=True, blank=True)),
            ],
            options={"ordering": ["name"], "verbose_name_plural": "families"},
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("order", models.SmallIntegerField(null=True, blank=True)),
                ("name", models.CharField(max_length=30)),
                ("suffix", models.CharField(max_length=3, null=True, blank=True)),
                (
                    "gender",
                    models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female")], null=True, blank=True),
                ),
                ("birthday", models.DateField(null=True, blank=True)),
                ("email", models.EmailField(max_length=254, null=True, blank=True)),
                ("phone_mobile", models.CharField(max_length=15, verbose_name="Mobile Phone", null=True, blank=True)),
                ("phone_work", models.CharField(max_length=15, verbose_name="Work Phone", null=True, blank=True)),
                ("is_member", models.BooleanField(default=True, verbose_name="Member")),
                ("is_current", models.BooleanField(default=True, verbose_name="Current")),
                ("family", models.ForeignKey(related_name="members", to="directory.Family", on_delete=models.CASCADE)),
                (
                    "user",
                    models.OneToOneField(
                        null=True, blank=True, on_delete=models.SET_NULL, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={"ordering": ["order", "id", "name"], "verbose_name_plural": "people"},
        ),
        migrations.AddField(
            model_name="family",
            name="husband",
            field=models.ForeignKey(
                related_name="+", blank=True, to="directory.Person", on_delete=models.SET_NULL, null=True
            ),
        ),
        migrations.AddField(
            model_name="family",
            name="wife",
            field=models.ForeignKey(
                related_name="+", blank=True, to="directory.Person", on_delete=models.SET_NULL, null=True
            ),
        ),
    ]
