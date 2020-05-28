from django.db import models
from django.contrib.auth import get_user_model
from django.utils.decorators import classonlymethod
from utils.models import BaseTimeStampField
from django_regex.fields import RegexField

User = get_user_model()
import re


# class MatchTypeChoice:
#     EXACT = 'exact'
#     IEXACT = 'iexact'
#     CONTAINS = 'contains'
#     ICONTAINS = 'icontains'
#     STARTSWITH = 'startswith'
#     ISTARTSWITH = 'istartswith'
#     ENDSWITH = 'endswith'
#     IENDSWITH = 'iendswith'
#
#     @classonlymethod
#     def get_chocies(cls):
#         return (
#             (cls.EXACT, 'Exact Match'),
#             (cls.IEXACT, 'iExact Match'),
#             (cls.CONTAINS, 'Contains Match'),
#             (cls.STARTSWITH, 'Startswith Match'),
#             (cls.ISTARTSWITH, 'iStartswith Match'),
#             (cls.ENDSWITH, 'endswith Match'),
#             (cls.IENDSWITH, 'iendswith Match'),
#         )
#
# MATCH_TYPE_LIST = MatchTypeChoice.get_chocies()

class TemplateForChoice:
    EMAIL_PARSING = 'E'
    QUEUE_PARSING = 'Q'
    BOTH_EMAIL_AND_QUEUE_PARSING = 'B'

    @classonlymethod
    def get_choices(cls):
        return (
            (cls.EMAIL_PARSING, 'Email Parsing'),
            (cls.QUEUE_PARSING, 'Queue Parsing'),
            (cls.BOTH_EMAIL_AND_QUEUE_PARSING, 'Both Email and Queue Parsing')
        )


class Template(BaseTimeStampField):

    EMAIL_PARSING = TemplateForChoice.EMAIL_PARSING
    QUEUE_PARSING = TemplateForChoice.QUEUE_PARSING
    BOTH_EMAIL_AND_QUEUE_PARSING = TemplateForChoice.BOTH_EMAIL_AND_QUEUE_PARSING

    template_for = models.CharField(max_length=10,
                                    choices=TemplateForChoice.get_choices(),
                                    default=TemplateForChoice.BOTH_EMAIL_AND_QUEUE_PARSING)
    title = models.CharField(max_length=75)
    domain = models.URLField(blank=True)
    email_from = models.EmailField(blank=True)
    email_to = models.EmailField(blank=True)
    subject = RegexField(max_length=128, null=True, flags=re.I, blank=True, help_text="regular expression field")
    user = models.ForeignKey(User, null=True, editable=False, on_delete=models.SET_NULL)
    desination = models.ForeignKey('destination.DestinationQueue', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.title


class Subject(BaseTimeStampField):
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='subjects')
    title = models.CharField(max_length=75)

    def __str__(self):
        return self.title


class ParsingTaskChoice:
    SUBJECT_PARSER = 'subject'
    BODY_PARSER = 'body'
    ATTACHMENT_PARSER = 'parser'

    @classonlymethod
    def get_choices(cls):
        return (
            (cls.SUBJECT_PARSER, 'Subject Parser'),
            (cls.BODY_PARSER, 'Email Body Parser'),
            (cls.ATTACHMENT_PARSER, 'Attachment  Parser'),
        )


class ParsingTask(BaseTimeStampField):
    template = models.ForeignKey(Template, null=True, on_delete=models.CASCADE, related_name='parsers')
    title = models.CharField(max_length=35, null=True)
    var_name = models.CharField(verbose_name="variable name", max_length=36, null=True)
    parser_type = models.CharField(verbose_name="Parser Type", max_length=75,
                                   choices=ParsingTaskChoice.get_choices())
    regex = RegexField(max_length=128, null=True, flags=re.I, help_text="regular expression field")
    desc = models.TextField(blank=True, editable=False)

    class Meta:
        verbose_name = 'parser'
        verbose_name_plural = 'parsers'

    def __str__(self):
        return self.title or str(self.pk)


class PDFTemplate(BaseTimeStampField):

    title = models.CharField(max_length=75)
    email_from = models.EmailField(blank=True)
    email_to = models.EmailField(blank=True)
    user = models.ForeignKey(User, null=True, editable=False, on_delete=models.SET_NULL)
    pdf_type = models.IntegerField(null=True)
    desination = models.ForeignKey('destination.DestinationQueue', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.title

class PDFParsingTask(BaseTimeStampField):
    template = models.ForeignKey(PDFTemplate, null=True, on_delete=models.CASCADE, related_name='pdfparsers')
    title = models.CharField(max_length=35, null=True)
    var_name = models.CharField(verbose_name="variable name", max_length=36, null=True)
    regex = RegexField(max_length=128, null=True, flags=re.I, help_text="regular expression field")
    desc = models.TextField(blank=True, editable=False)

    class Meta:
        verbose_name = 'pdfparser'
        verbose_name_plural = 'pdfparsers'

    def __str__(self):
        return self.title or str(self.pk)
