from rest_framework import serializers
from . import models


class OrgansSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organization
        fields = [
            'pk',
            'province',
            'name',
            'organization_phone',
            'employees_number',
            'owner',
            'email',
            'owner_phone',
            'organization_product',
        ]
