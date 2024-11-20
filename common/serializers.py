from rest_framework.serializers import (
    ModelSerializer,
)

class ListSerializer(ModelSerializer):

    class Meta:
        ref_name = ""
        fields = (
            "id",
            "slug",

        )
        read_only_fields = (
            "id",
            "slug"
        )
