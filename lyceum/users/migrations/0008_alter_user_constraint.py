from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_alter_profile_bio"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="user",  # или напрямую через RunSQL на auth_user
            constraint=models.UniqueConstraint(
                fields=["email"], name="unique_email"
            ),
        ),
    ]
