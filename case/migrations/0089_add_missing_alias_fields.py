from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    dependencies = [
        ('case', '0088_remove_mortgageneeds_is_ability_to_add_fees_mortgage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loandetails',
            name='alias',
            field=models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True),
        ),
    ]