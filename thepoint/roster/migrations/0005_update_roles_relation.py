# pylint: disable=invalid-name
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("roster", "0004_set_on_delete"),
    ]

    operations = [
        migrations.AlterField(
            model_name="role",
            name="people",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={"is_current": True},
                related_name="roles",
                to="directory.Person",
                verbose_name="people",
            ),
        ),
    ]
