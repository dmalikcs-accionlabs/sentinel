from rest_framework import serializers, status
from .models import EmailCollection

class EmailCollectSerializer(serializers.ModelSerializer):
    # to = serializers.EmailField(source='to_email_id')

    class Meta:
        model = EmailCollection
        fields= ('email_to','email_from','body','subject')