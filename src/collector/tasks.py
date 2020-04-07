from sentinel.celery import app
from celery import Task
from .models import EmailCollection
from django.core.exceptions import ObjectDoesNotExist

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
            print(e)
        except ObjectDoesNotExist:
            pass
        return email_id

    def on_success(self, retval, task_id, args, kwargs):
        print("Update the ELK loggin")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print("Update the error logs to ELK loggin")


class ExecuteParserTask(Task):
    name = 'execute_parser'

    def run(self, *args, **kwargs):
        print("Execute parser from template")
        email_id = args[0]
        print(email_id)
        return email_id

    def on_success(self, retval, task_id, args, kwargs):
        print("Update  Execution parser")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print("Update failure logs to ELK")


class PublishToSBTask(Task):

    name = 'pusblish_to_sb'

    def run(self,  *args, **kwargs):
        #             connection_str = \
        #                 'Endpoint=sb://dynastydev.servicebus.windows.net/;SharedAccessKeyName=CancelledOrders;SharedAccessKey=QyZ7PCAb3ofM4UbQMux0LFy0otDh0PqqDy33DthoaLU='
        #             sb_client = ServiceBusClient.from_connection_string(connection_str)
        #             queue_client = sb_client.get_queue("CancelledOrders")
        #             queue_client.send(Message(json.dumps( {
        #                 "CreationDate": "2020-04-03T13:12:32.6879998-03:00",
        #                 "MessageType": 0,
        #                 "Content": {
        #                     "SenderAddress": self.email_from,
        #                     "EmailDate": "2020-03-25T13:12:32.6887854-03:00",
        #                     "OrderNumber": "20255033"
        #                 }
        #             })))
        print("Publish tasks")
        email_id = args[0]
        print(email_id)
        return email_id

    def on_success(self, retval, task_id, args, kwargs):
        print("Update success logs")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print("Update failure logs")


app.tasks.register(MatchTemplateTask())
app.tasks.register(ExecuteParserTask())
app.tasks.register(PublishToSBTask())

