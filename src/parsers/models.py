from django.db import models
from django.contrib.auth import get_user_model
from django.utils.decorators import classonlymethod
from utils.models import BaseTimeStampField

User = get_user_model()


class MatchTypeChoice:
    EXACT = 'exact'
    IEXACT = 'iexact'
    CONTAINS = 'contains'
    ICONTAINS = 'icontains'
    STARTSWITH = 'startswith'
    ISTARTSWITH = 'istartswith'
    ENDSWITH = 'endswith'
    IENDSWITH = 'iendswith'

    @classonlymethod
    def get_chocies(cls):
        return (
            (cls.EXACT, 'Exact Match'),
            (cls.IEXACT, 'iExact Match'),
            (cls.CONTAINS, 'Contains Match'),
            (cls.STARTSWITH, 'Startswith Match'),
            (cls.ISTARTSWITH, 'iStartswith Match'),
            (cls.ENDSWITH, 'endswith Match'),
            (cls.IENDSWITH, 'iendswith Match'),
        )

MATCH_TYPE_LIST = MatchTypeChoice.get_chocies()


class Template(BaseTimeStampField):
    title = models.CharField(max_length=75)
    parser = models.ForeignKey('parsers.ParsingTask', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, null=True, editable=False, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class Subject(BaseTimeStampField):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    match_type = models.CharField(max_length=35, choices=MATCH_TYPE_LIST)

    def __str__(self):
        return self.title


class ParsingTaskChoice:
    STUBHUB_SUBJECT_PARSER = 'stubhub_subject_parser'
    TICKETMASTER_SUBJECT_PARSER = 'ticketmaster_subject_parser'
    STUBHUB_BODY_PARSER = 'stubhub_body_parser'

    @classonlymethod
    def get_choices(cls):
        return (
            (cls.STUBHUB_SUBJECT_PARSER, 'Stubhub cancel order'),
            (cls.TICKETMASTER_SUBJECT_PARSER,'Ticketmaster cancel order'),
            (cls.STUBHUB_BODY_PARSER,'Stubhub cancel order')
        )


class ParsingTask(BaseTimeStampField):
    parser = models.CharField(max_length=75, choices=ParsingTaskChoice.get_choices())
    desc = models.TextField(blank=True)

    def __str__(self):
        return self.get_parser_display()

    def get_parser_class(self):
        if self.parser == ParsingTaskChoice.STUBHUB_SUBJECT_PARSER:
            return
        else:
            return ''

