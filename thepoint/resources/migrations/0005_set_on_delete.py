# pylint: disable=invalid-name
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resources", "0004_localise_strings"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resource",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.SET_NULL,
                related_name="resources",
                to="directory.Person",
                verbose_name="author",
            ),
        ),
        migrations.AlterField(
            model_name="resource",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.SET_NULL,
                related_name="children",
                to="resources.Resource",
                verbose_name="parent",
            ),
        ),
    ]
