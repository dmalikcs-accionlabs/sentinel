from sentinel.celery import app
from celery import Task
from .models import EmailCollection, TemplateMatchStatusChoice, \
    SBEmailParsing, PDFCollection, PDFData
from parsers.models import Template, \
    ParsingTaskChoice, PDFTemplate
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

    def get_model(self, m):
        if m == SBEmailParsing.__name__:
            return SBEmailParsing
        elif m == EmailCollection.__name__:
            return EmailCollection
        else:
            return None

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
            templates = []
            id = args[0]
            model = self.get_model(args[1])

            e = model.objects.get(id=id)
            return_dict = {'id': id, 'model': args[1]}
            if not e:
                return return_dict
            kw = {}
            fields = e.get_matching_fields()
            # IS_MULTIPLE_TEMPLATES = None


            # kw_q = {field: getattr(e, map_field) for field, map_field in fields.items()}
            # print(Template.objects.filter(**kw_q) | Template.objects.filter(**kw_q))

            matched_templates = None

            for field, map_field in fields.items():
                f = getattr(e, map_field)
                kw.update({
                    field: f,
                    'template_for__in': [e.get_template_for(),  Template.BOTH_EMAIL_AND_QUEUE_PARSING],
                    'deleted__isnull': True
                })
                template_query = Template.objects.filter(**kw)
                print(kw)
                print(template_query)
                if template_query.exists():
                    matched_templates = template_query

                # IS_MULTIPLE_TEMPLATES = False


                # q1 = Template.objects.filter(**kw)
                # kw.update({
                #     'template_for': Template.,
                #
                # })
                # both_qs = Template.objects.filter(**kw)
                # q = q1.union(both_qs,  all=False)
            if matched_templates.count() == 1:
                e.template_match_status = TemplateMatchStatusChoice.TEMPLATE_MATCH_FOUND
                e.template = matched_templates[0]
                e.save()
                # IS_MULTIPLE_TEMPLATES = False
                # break;
            elif matched_templates.count() > 1:
                subjects = []
                for s in matched_templates:
                    templates.append(s)
                    if not s.subject:
                        continue
                    try:
                        match = s.subject.match(e.subject)
                        if match:
                            subjects.append(s)
                    except Exception as e:
                        print(e)
                if len(subjects) == 1:
                    t = subjects[0]
                    e.template = t
                    e.template_match_status = TemplateMatchStatusChoice.TEMPLATE_MATCH_FOUND
                    e.save()
                    # IS_MULTIPLE_TEMPLATES = False
                    # break
                elif len(subjects) > 1:
                    e.template_match_status = TemplateMatchStatusChoice.MULTIPLE_TEMPLATE_MATCH
                    e.save()
                    e.match_templates.add(*subjects)
                else:
                    e.template_match_status = TemplateMatchStatusChoice.MULTIPLE_TEMPLATE_MATCH
                    e.save()
                    e.match_templates.add(*templates)
            else:
                e.template_match_status = TemplateMatchStatusChoice.NO_TEMPLATE_MATCH
                e.save()
                # break

            if e.template_match_status == TemplateMatchStatusChoice.MULTIPLE_TEMPLATE_MATCH:
                if e.match_templates.all().exists():
                    e.template = e.match_templates.last()
                    e.save()
            log_fields = dict()

            log_fields[EMAILLoggingChoiceField.TASK] = self.name
            log_fields[EMAILLoggingChoiceField.STATUS] = "Completed"
            logger.info(e.get_template_match_status_display(), log_fields)
            return return_dict
        except ObjectDoesNotExist:
            log_fields = dict()
            log_fields['index-name'] = os.environ.get('LOG_INDEX_NAME',
                                                      'sentinel-email-parser')
            log_fields[EMAILLoggingChoiceField.TASK] = self.name
            log_fields[EMAILLoggingChoiceField.STATUS] = "Failed"
            logger.error("No Email object found", extra=log_fields)
        return return_dict


class ExecuteParserTask(Task):
    name = 'execute_parser'

    def get_model(self, m):
        if m == SBEmailParsing.__name__:
            return SBEmailParsing
        elif m == EmailCollection.__name__:
            return EmailCollection
        else:
            return None

    def run(self, *args, **kwargs):
        print(args)
        print(kwargs)
        try:
            if not args:
                raise ObjectDoesNotExist
            kw = args[0]
            id = kw.get('id')
            model = kw.get('model')
            m = self.get_model(model)
            extracted_fields = {}
            e = m.objects.get(id=id)
            if e.template:
                parsers = e.template.parsers.all()
                for parser in parsers:
                    if parser.parser_type == ParsingTaskChoice.SUBJECT_PARSER:
                        matches = parser.regex.findall(e.subject)
                        if matches:
                            extracted_fields.update({parser.var_name: matches[0]})
                    elif parser.parser_type == ParsingTaskChoice.BODY_PARSER:
                        if e.body_type == 'html':
                            soup = BeautifulSoup(e.html)
                            clean_text = soup.get_text()
                        elif e.body_type == 'text':
                            clean_text = e.body
                        else:
                            raise ObjectDoesNotExist
                        search_text = list()
                        if e.template.multiple_events:
                            search_text = clean_text.split(e.template.event_split_string)
                        else:
                            search_text.append(clean_text)
                        for i in range(len(search_text)):
                            matches = parser.regex.findall(search_text[i])
                            if matches :
                                extracted_values = dict()
                                if parser.get_multiple_values:
                                    extracted_values[parser.var_name] = matches

                                else:
                                    extracted_values[parser.var_name] =matches[0]
                                if i in extracted_fields.keys():
                                    extracted_fields[i].update(extracted_values)
                                else:
                                    extracted_fields.update({i:extracted_values})
                    else:
                        pass

            if extracted_fields:
                for event, data in extracted_fields.items():
                    if not isinstance(data, dict):
                        continue
                    a = [dict() for i in range(len(list(data.values())[0]))]
                    for key, value in data.items():
                        if not isinstance(value, list):
                            a = extracted_fields[event]
                            continue
                        for i in range(len(value)):
                            a[i].update({key: data[key][i]})
                    extracted_fields[event] = a
                e.meta = extracted_fields
                e.save()

                publish = PublishToSBTask()
                publish.delay(id=id, model=model)
            # log_fields = get_email_log_variable(e)
            # log_fields[EMAILLoggingChoiceField.TASK] = self.name
            # log_fields[EMAILLoggingChoiceField.STATUS] = "Completed"
            # logger.info("Parsers Executed and extracted variables are "
            #                  "added to meta field of Email Object",
            #              extra=log_fields)
            log_fields = dict()
            log_fields[EMAILLoggingChoiceField.TASK] = self.name
            log_fields[EMAILLoggingChoiceField.STATUS] = "Completed"
            logger.info("Parsers Executed and extracted variables are "
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

    def get_model(self, m):
        if m == SBEmailParsing.__name__:
            return SBEmailParsing
        elif m == EmailCollection.__name__:
            return EmailCollection
        else:
            return None

    def run(self, *args, **kwargs):
        print(kwargs)
        try:
            if not kwargs:
                raise ObjectDoesNotExist
            id = kwargs.get('id')
            model = kwargs.get('model')
            m = self.get_model(model)
            e = m.objects.get(id=id)
            log_fields = dict()
            log_fields[EMAILLoggingChoiceField.TASK] = self.name
            is_published, error = e.publish_order()
            if is_published:
                e.is_published = True
                e.save()
                log_fields[EMAILLoggingChoiceField.STATUS] = "Completed"
                logger.info("published to the {} queue".format(
                    e.template.desination), extra=log_fields)
            else:
                print(error)
                log_fields[EMAILLoggingChoiceField.STATUS] = "fail"
                log_fields['Error'] = error
                logger.info("Failed to published on the {} queue".format(
                    e.template.desination), extra=log_fields)
            # log_fields = get_email_log_variable(e)
            # log_fields[EMAILLoggingChoiceField.TASK] = self.name
            # log_fields[EMAILLoggingChoiceField.STATUS] = "Completed"
            # logger.info("published to the {} queue".format(
            #     e.template.desination), extra=log_fields)
        except ObjectDoesNotExist:
            log_fields = dict()
            log_fields['index-name'] = os.environ.get('LOG_INDEX_NAME',
                                                      'sentinel-email-parser')
            log_fields[EMAILLoggingChoiceField.TASK] = self.name
            log_fields[EMAILLoggingChoiceField.STATUS] = "Failed"
            logger.error("Email Object ID Not Passed ", extra=log_fields)


class PDFMatchTemplateTask(Task):
    """
    PDFMatchTemplateTask class is a celery task to select parser for the PDF
    """
    name = 'pdf_match_template'

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
            id = args[0]
            pdf_obj = PDFCollection.objects.get(id=id)
            return_dict = {'id': id}
            if not pdf_obj:
                return return_dict
            kw = {}
            fields = pdf_obj.get_matching_fields()
            IS_MULTIPLE_TEMPLATES = None
            matched_templates = None
            for field, map_field in fields.items():
                IS_MULTIPLE_TEMPLATES = False
                f = getattr(pdf_obj, map_field)

                kw.update({field: f,})
                q = PDFTemplate.objects.filter(**kw)
                matched_templates = q
            if matched_templates.count() == 1:
                pdf_obj.template_match_status = TemplateMatchStatusChoice.TEMPLATE_MATCH_FOUND
                pdf_obj.template = matched_templates[0]
                pdf_obj.match_templates.add(*matched_templates)
                pdf_obj.save()
                IS_MULTIPLE_TEMPLATES = False
            elif matched_templates.count() > 1:
                IS_MULTIPLE_TEMPLATES = True
                pdf_obj.match_templates.add(*matched_templates)
            else:
                pdf_obj.template_match_status = TemplateMatchStatusChoice.NO_TEMPLATE_MATCH
                pdf_obj.save()
            if IS_MULTIPLE_TEMPLATES:
                pdf_obj.template_match_status = TemplateMatchStatusChoice.MULTIPLE_TEMPLATE_MATCH
                pdf_obj.save()
            log_fields = dict()
            log_fields[EMAILLoggingChoiceField.TASK] = self.name
            log_fields[EMAILLoggingChoiceField.STATUS] = "Completed"
            logger.info(pdf_obj.get_template_match_status_display(), log_fields)
            return return_dict
        except ObjectDoesNotExist:
            log_fields = dict()
            log_fields['index-name'] = os.environ.get('LOG_INDEX_NAME',
                                                      'sentinel-email-parser')
            log_fields[EMAILLoggingChoiceField.TASK] = self.name
            log_fields[EMAILLoggingChoiceField.STATUS] = "Failed"
            logger.error("No Email object found", extra=log_fields)
        return return_dict


class PDFExecuteParserTask(Task):
    name = 'pdf_execute_parser'

    def run(self, *args, **kwargs):
        try:
            if not args:
                raise ObjectDoesNotExist
            kw = args[0]
            id = kw.get('id')
            extracted_fields = {}
            pdf_obj = PDFCollection.objects.get(id=id)
            if pdf_obj.template:
                parsers = pdf_obj.template.pdfparsers.all()
                pdf_pages = PDFData.objects.filter(pdf=pdf_obj)
                publish_to_SB = False
                for page in pdf_pages:
                    for parser in parsers:
                        matches = parser.regex.findall(page.content)
                        if matches:
                            extracted_fields.update({parser.var_name: matches[0]})
                    if extracted_fields:
                        publish_to_SB = True
                        page.meta = extracted_fields
                        page.save()
                if publish_to_SB:
                    publish = PDFPublishToSBTask()
                    publish.delay(id=id)
            log_fields = dict()
            log_fields[EMAILLoggingChoiceField.TASK] = self.name
            log_fields[EMAILLoggingChoiceField.STATUS] = "Completed"
            logger.info("Parsers Executed and extracted variables are "
                        "added to meta field of Email Object",
                        extra=log_fields)
        except ObjectDoesNotExist:
            log_fields = dict()
            log_fields['index-name'] = os.environ.get('LOG_INDEX_NAME',
                                                      'sentinel-email-parser')
            log_fields[EMAILLoggingChoiceField.TASK] = self.name
            log_fields[EMAILLoggingChoiceField.STATUS] = "Failed"
            logger.error("No Email object found", extra=log_fields)


class PDFPublishToSBTask(Task):
    name = 'pdf_pusblish_to_sb'

    def run(self, *args, **kwargs):
        try:
            if not kwargs:
                raise ObjectDoesNotExist
            id = kwargs.get('id')
            pdf_obj= PDFCollection.objects.get(pk=id)
            log_fields = dict()
            log_fields[EMAILLoggingChoiceField.TASK] = self.name
            is_published, error = pdf_obj.publish_order()
            if is_published:
                pdf_obj.is_published = True
                pdf_obj.save()
                log_fields[EMAILLoggingChoiceField.STATUS] = "Completed"
                logger.info("published to the {} queue".format(
                    pdf_obj.template.desination), extra=log_fields)
            else:
                log_fields[EMAILLoggingChoiceField.STATUS] = "fail"
                log_fields['Error'] = error
                logger.info("Failed to published on the {} queue".format(
                    pdf_obj.template.desination), extra=log_fields)
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
app.tasks.register(PDFMatchTemplateTask())
app.tasks.register(PDFExecuteParserTask())
app.tasks.register(PDFPublishToSBTask())

