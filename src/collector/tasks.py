from sentinel.celery import app
from celery import Task
from .models import EmailCollection
from parsers.models import Template
from django.core.exceptions import ObjectDoesNotExist
from azure.servicebus import QueueClient, Message, ServiceBusClient
from custom_logging.custom_logging import get_email_log_variable
from custom_logging.choices import EMAILLoggingChoiceField
import json
import logging

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
            email_id = args[0]
            e = EmailCollection.objects.get(id=email_id)
            kw = {}
            fields = ['email_from', 'email_to']
            for field in fields:
                f = getattr(e, field)

                kw.update({field: f})
                q = Template.objects.filter(**kw)
                if q.count() == 1:
                    e.template = q[0]
                    e.parser = q[0].parser
                    e.save()
                    break;
                elif q.count() > 1:
                    subjects = {}
                    for s in q:
                        print(s, s.subject, e.subject)
                        try:
                            match = s.subject.match(e.subject)
                            if match:
                                subjects.update({s: match})
                        except Exception as e:
                            print(e)
                    if len(subjects) == 1:
                        t = next(iter(subjects.keys()))
                        e.template = t
                        e.parser = t.parser
                        e.save()
                        break
                else:
                    break
        except ObjectDoesNotExist:
            pass
        return email_id

    def on_success(self, retval, task_id, args, kwargs):

        log_fields = get_log_fields(args[0])
        if log_fields['template'] is None:
            msg = " template and Parser not mapped"
        else:
            msg = " mapped to template {}".format(log_fields['template'])
            if log_fields['parser'] is None :
                msg += " but not mapped to any parser"
            else:
                msg += "and parser {}".format(log_fields['parser'])
        log_fields[EMAILLoggingChoiceField.TASK] = self.name
        log_fields[EMAILLoggingChoiceField.STATUS] = "Completed"
        logger.info(msg=msg,extra=log_fields)


    def on_failure(self, exc, task_id, args, kwargs, einfo):
        log_fields = get_log_fields(args[0])
        log_fields[EMAILLoggingChoiceField.TASK] = self.name
        log_fields[EMAILLoggingChoiceField.STATUS] = "Failed"
        logger.info(msg=einfo, extra=log_fields)


class ExecuteParserTask(Task):
    name = 'execute_parser'

    def run(self, *args, **kwargs):
        email_id = args[0]
        e = EmailCollection.objects.get(id=email_id)
        if e.parser:
            print("Calling Parser")
            parser = e.parser
            txt = getattr(e, parser.parser)
            print("{}:{}".format(parser.parser, txt))
            d = parser.regex.findall(txt)
            if d:
                return {'email_id': email_id, 'order_id': d[0]}

    def on_success(self, retval, task_id, args, kwargs):
        log_fields = get_log_fields(args[0])
        log_fields[EMAILLoggingChoiceField.TASK] = self.name
        log_fields[EMAILLoggingChoiceField.STATUS] = "Completed"
        logger.info ("",extra=log_fields)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        log_fields = get_log_fields(args[0])
        log_fields[EMAILLoggingChoiceField.TASK] = self.name
        log_fields[EMAILLoggingChoiceField.STATUS] = "Failed"
        logger.info(einfo, extra=log_fields)


class PublishToSBTask(Task):
    name = 'pusblish_to_sb'

    def run(self, *args, **kwargs):
        if not args:
            return

        kw = args[0]
        email_id = kw.get('email_id')
        order_id = kw.get('order_id')
        e = EmailCollection.objects.get(id=email_id)
        e.publish_order(order_id)

    def on_success(self, retval, task_id, args, kwargs):
        kw = args[0]
        log_fields = get_log_fields(kw.get('email_id'))
        msg = "publieshed the order number {}".format(kw.get('order_id'))
        log_fields[EMAILLoggingChoiceField.TASK] = self.name
        log_fields[EMAILLoggingChoiceField.STATUS] = "Completed"
        logger.info (msg,extra=log_fields)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        kw = args[0]
        log_fields = dict()
        if kw and kw.get('email_id'):
            log_fields = get_log_fields(kw.get('email_id'))
            msg = einfo
        else:
            msg =" EMAIl ID and Order id not passed as arguments "
        log_fields[EMAILLoggingChoiceField.TASK] = self.name
        log_fields[EMAILLoggingChoiceField.STATUS] = "Failed"
        logger.info(msg, extra=log_fields)


def get_log_fields(email_id):
    e = EmailCollection.objects.get(id=email_id)
    return get_email_log_variable(e)


app.tasks.register(MatchTemplateTask())
app.tasks.register(ExecuteParserTask())
app.tasks.register(PublishToSBTask())
