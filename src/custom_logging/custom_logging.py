from django.forms.models import model_to_dict
from custom_logging.choices import EMAILLoggingChoiceField
from collector.models import EmailAttachment
import os

index_name = os.environ.get('LOG_INDEX_NAME', 'Sentinel-Email-Parser')

def get_email_log_variable(email_collection_obj):

    log_fields = model_to_dict(email_collection_obj)
    log_fields['index-name'] = index_name
    if log_fields.get(EMAILLoggingChoiceField.LOCATION):
        log_fields[EMAILLoggingChoiceField.LOCATION]=str(
            log_fields[EMAILLoggingChoiceField.LOCATION])
    attachments = EmailAttachment.objects.filter(email=email_collection_obj.pk)
    log_fields[EMAILLoggingChoiceField.ATTACHMENT_COUNT] = len(attachments)
    # log_fields[EMAILLoggingChoiceField.EMAIL_DATE] = email_collection_obj.email_date

    return log_fields