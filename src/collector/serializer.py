from rest_framework import serializers, fields

from .models import SBEmailParsing, PDFCollection


class SBEmailParsingSerilizers(serializers.ModelSerializer):
    ClientId = fields.CharField(source="client_id")
    UniqueIdentifier = fields.CharField(source="unique_identifier")
    Subject = fields.CharField(source="subject")
    InboxUsername = fields.CharField(source='inbox_username', max_length=128)
    BodyPlainText = fields.CharField(allow_blank=True, source='body_plaintext', required=False, style={'base_template': 'textarea.html'})
    BodyHtmlContent = fields.CharField(allow_blank=True, source='body_html_content', required=False, style={'base_template': 'textarea.html'})
    FromAddress = fields.EmailField(source='from_address', max_length=254)
    ToAddresses = fields.EmailField(source='to_addresses', max_length=254)

    class Meta:
        model = SBEmailParsing
        fields = ['ClientId', 'UniqueIdentifier', 'InboxUsername', 'Subject',
                  'BodyPlainText', 'BodyHtmlContent', 'FromAddress',
                  'ToAddresses']

class PDFCollectionSerilizers(serializers.ModelSerializer):
    clientId = fields.CharField(source="client_id")
    fromEmail = fields.EmailField(source='from_address', max_length=254)
    toEmail = fields.EmailField(source='to_addresses', max_length=254)
    pdfLink = fields.CharField(source='location')
    number_of_pages = fields.IntegerField()
    typeId = fields.IntegerField(source='type_id')

    class Meta:
        model = PDFCollection
        fields = ['clientId', 'fromEmail', 'toEmail', 'pdfLink',
                  'number_of_pages', 'typeId']
