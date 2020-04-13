from django.forms.models import model_to_dict
from custom_logging.choices import EMAILLoggingChoiceField
from collector.models import EmailAttachment
import os

index_name = os.environ.get('LOG_INDEX_NAME', 'Sentinel-Email-Parser')

def get_email_log_variable(email_obj):

    log_fields = model_to_dict(email_obj)
    log_fields['index-name'] = index_name
    if log_fields.get(EMAILLoggingChoiceField.LOCATION):
        log_fields[EMAILLoggingChoiceField.LOCATION]=str(
            log_fields[EMAILLoggingChoiceField.LOCATION])
    if log_fields.get(EMAILLoggingChoiceField.TEMPLATE) is not None:
        log_fields[EMAILLoggingChoiceField.TEMPLATE] = str(email_obj.template.title)
    if log_fields.get(EMAILLoggingChoiceField.PARSER) is not None:
        log_fields[EMAILLoggingChoiceField.PARSER] = str(email_obj.parser.title)
    log_fields[EMAILLoggingChoiceField.ATTACHMENT_COUNT] = email_obj.attachments_count
    log_fields[EMAILLoggingChoiceField.EMAIL_DATE] = email_obj.email_date
    log_fields[EMAILLoggingChoiceField.EMAIL_TO] = email_obj.email_to
    log_fields[EMAILLoggingChoiceField.CC] = email_obj.cc
    return log_fields