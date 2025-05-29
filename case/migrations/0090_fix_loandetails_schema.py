from django.db import migrations, models
import uuid
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ("case", "0089_add_missing_alias_fields"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='loandetails',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='loandetails',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='loandetails',
            name='created_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='created_loandetails_set',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Created By',
            ),
        ),
        migrations.AddField(
            model_name='loandetails',
            name='updated_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='updated_loandetails_set',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Updated By',
            ),
        ),
        migrations.AddField(
            model_name='loandetails',
            name='user_ip',
            field=models.GenericIPAddressField(blank=True, editable=False, null=True),
        ),
    ]

