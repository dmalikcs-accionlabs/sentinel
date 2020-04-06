from rest_framework import serializers, status
from .models import EmailData

class EmailDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailData
        fields= ('to_email_id','from_email_id','body','email_date','email_envelope','subject')
    def create(self, validated_data):
        """
        Insert ingestion data to database
        :param validated_data:
        :return:
        """
        instance = EmailData.objects.create(**validated_data)
        return instance

