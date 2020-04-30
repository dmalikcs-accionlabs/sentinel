from sentinel.celery import app
from celery import Task
from .models import EmailCollection, TemplateMatchStatusChoice
from parsers.models import Template, \
    ParsingTaskChoice
from django.core.exceptions import ObjectDoesNotExist
from azure.servicebus import QueueClient, Message, ServiceBusClient
from custom_logging.custom_logging import get_email_log_variable
from custom_logging.choices import EMAILLoggingChoiceField
from bs4 import BeautifulSoup
import json
import logging
import os

logger = logging.getLogger('sentinel')


class MatchTemplateTask(Task):
    """
    MatchTemplateTask class is a celery task to select parser
    """
    name = 'match_template'

    def run(self, *args, **kwargs):
        """
        Executes process
        :param args:
        :param kwargs:
        :return: ingestion id
        """
        try:
            if not args:
                raise ObjectDoesNotExist
            email_id = args[0]
            e = EmailCollection.objects.get(id=email_id)
            kw = {}
            fields = ['email_from', ]
            IS_MULTIPLE_TEMPLATES = None
            for field in fields:
                IS_MULTIPLE_TEMPLATES = False
                f = getattr(e, field)

                kw.update({field: f})
                q = Template.objects.filter(**kw)
                if q.count() == 1:
                    e.template_match_status = TemplateMatchStatusChoice.TEMPLATE_MATCH_FOUND
                    e.template = q[0]
                    e.save()
                    IS_MULTIPLE_TEMPLATES = False
                    break;
                elif q.count() > 1:
                    subjects = {}
                    for s in q:
                        try:
                            match = s.subject.match(e.subject)
                            if match:
                                subjects.update({s: match})
                        except Exception as e:
                            print(e)
                    if len(subjects) == 1:
                        t = next(iter(subjects.keys()))
                        e.template = t
                        e.template_match_status = TemplateMatchStatusChoice.TEMPLATE_MATCH_FOUND
                        e.save()
                        IS_MULTIPLE_TEMPLATES = False
                        break
                    else:
                        IS_MULTIPLE_TEMPLATES = True
                else:
                    e.template_match_status = TemplateMatchStatusChoice.NO_TEMPLATE_MATCH
                    e.save()
                    break
            if IS_MULTIPLE_TEMPLATES:
                e.template_match_status = TemplateMatchStatusChoice.MULTIPLE_TEMPLATE_MATCH
                e.save()
            log_fields = get_email_log_variable(e)
            log_fields[EMAILLoggingChoiceField.TASK] = self.name
            log_fields[EMAILLoggingChoiceField.STATUS] = "Completed"
            logger.info(e.get_template_match_status_display(), log_fields)
            return email_id
        except ObjectDoesNotExist :
            log_fields = dict()
            log_fields['index-name'] = os.environ.get('LOG_INDEX_NAME',
                                                      'sentinel-email-parser')
            log_fields[EMAILLoggingChoiceField.TASK] = self.name
            log_fields[EMAILLoggingChoiceField.STATUS] = "Failed"
            logger.error("No Email object found", extra=log_fields)
        return email_id


class ExecuteParserTask(Task):
    name = 'execute_parser'

    def run(self, *args, **kwargs):
        try :
            if not args:
                raise ObjectDoesNotExist
            email_id = args[0]
            extracted_fields = {}
            e = EmailCollection.objects.get(id=email_id)
            if e.template:
                parsers = e.template.parsers.all()
                for parser in parsers:
                    if parser.parser_type == ParsingTaskChoice.SUBJECT_PARSER:
                        matches = parser.regex.findall(e.subject)
                        print(matches)
                        if matches:
                            extracted_fields.update({parser.var_name: matches[0]})
                    elif parser.parser_type == ParsingTaskChoice.BODY_PARSER \
                            and e.body_type == 'text':
                        matches = parser.regex.findall(e.body)
                        if matches:
                            extracted_fields.update({parser.var_name: matches[0]})
                    elif parser.parser_type == ParsingTaskChoice.BODY_PARSER \
                            and e.body_type == 'html':
                        soup = BeautifulSoup(e.html)
                        clean_text = soup.get_text()
                        matches = parser.regex.findall(clean_text)
                        if matches:
                            extracted_fields.update({parser.var_name: matches[0]})
                    else:
                        pass

            if extracted_fields:
                e.meta = extracted_fields
                e.save()

                publish = PublishToSBTask()
                publish.delay({'email_id': e.pk})
            log_fields = get_email_log_variable(e)
            log_fields[EMAILLoggingChoiceField.TASK] = self.name
            log_fields[EMAILLoggingChoiceField.STATUS] = "Completed"
            logger.info( "Parsers Executed and extracted variables are "
                             "added to meta field of Email Object",
                         extra=log_fields)
        except ObjectDoesNotExist:
            log_fields = dict()
            log_fields['index-name'] = os.environ.get('LOG_INDEX_NAME',
                                                      'sentinel-email-parser')
            log_fields[EMAILLoggingChoiceField.TASK] = self.name
            log_fields[EMAILLoggingChoiceField.STATUS] = "Failed"
            logger.error("No Email object found", extra=log_fields)


class PublishToSBTask(Task):
    name = 'pusblish_to_sb'

    def run(self, *args, **kwargs):
        try:
            if not args:
                raise ObjectDoesNotExist
            kw = args[0]
            email_id = kw.get('email_id')
            e = EmailCollection.objects.get(id=email_id)
            e.publish_order()
            log_fields = get_email_log_variable(e)
            log_fields[EMAILLoggingChoiceField.TASK] = self.name
            log_fields[EMAILLoggingChoiceField.STATUS] = "Completed"
            logger.info("published to the {} queue".format(
                e.template.desination), extra=log_fields)
        except ObjectDoesNotExist:
            log_fields = dict()
            log_fields['index-name'] = os.environ.get('LOG_INDEX_NAME',
                                                      'sentinel-email-parser')
            log_fields[EMAILLoggingChoiceField.TASK] = self.name
            log_fields[EMAILLoggingChoiceField.STATUS] = "Failed"
            logger.error("Email Object ID Not Passed ", extra=log_fields)





app.tasks.register(MatchTemplateTask())
app.tasks.register(ExecuteParserTask())
app.tasks.register(PublishToSBTask())
