from django.db import models
from django.contrib.auth import get_user_model
from django.utils.decorators import classonlymethod
User =  get_user_model()


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


class BaseTimeStampField(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(editable=False, null=True)

    class Meta:
        abstract = True


class Template(BaseTimeStampField):
    title = models.CharField(max_length=75)
    user = models.ForeignKey(User, null=True, editable=False, on_delete=models.SET_NULL)


class Subject(BaseTimeStampField):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    match_type = models.CharField(max_length=35, choices=MATCH_TYPE_LIST)
