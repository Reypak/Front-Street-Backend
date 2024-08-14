# Migrations

## Handling migration with existing data

### For non-null fields

First, add the OneToOneField to the Profile model and set null=True. This allows the migration to occur without requiring a profile for each user immediately.

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    # Then run migrations
```

### Generate an empty migration.

```sh
python manage.py makemigrations --empty fs_profiles  --name populate_profiles
```

### Open and Modify the migration

```python
from django.db import migrations


def create_profiles(apps, schema_editor):
    CustomUser = apps.get_model('fs_users', 'CustomUser')
    Profile = apps.get_model('fs_profiles', 'Profile')

    # create a profile for each user
    for user in CustomUser.objects.all():
        Profile.objects.create(user=user)


class Migration(migrations.Migration):

    dependencies = [
        ('fs_profiles', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_profiles),
    ]
```

### Apply the migration to populate the `Profile` model.

```sh
python manage.py migrate
```

### Make the `user` Field Non-Nullable

Now that every user has a corresponding profile, make the `user` field non-nullable.

```python
user = models.OneToOneField(User, on_delete=models.CASCADE)
# Then run migrations
```
