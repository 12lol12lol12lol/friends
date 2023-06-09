from django.db import migrations


def create_default_users(apps, schema_editor):
    """Create test users """
    from django.contrib.auth import get_user_model

    Model = apps.get_model('user', 'User')
    Model.objects.create_user(
        username='test_user1',
        password='testuserpassword1',
    )
    Model.objects.create_user(
        username='test_user2',
        password='testuserpassword2',
    )
    


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_users),
    ]