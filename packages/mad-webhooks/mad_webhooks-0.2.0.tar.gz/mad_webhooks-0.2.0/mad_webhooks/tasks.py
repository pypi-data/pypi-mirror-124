from mad_webhooks.utils import postEventToWebhooks
from mad_webhooks.models import Event, Log, WebhookEventPostAttempt, Webhook
from celery import shared_task
import json
import requests
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model


@shared_task(name="Non-Periodic: Post Event to Webhooks", soft_time_limit=50000, time_limit=80000)
def postEventToWebhook(event_id):
    """ Post the event to webhook """
    # get event Details
    event = Event.objects.get(id=event_id)

    # post to application webhooks
    if event.application is not None:
        # get webhook endpoint urls from application
        webhooks = Webhook.objects.filter(application=event.application, is_active=True)
        postEventToWebhooks(event, webhooks)

    return "Processed event " + str(event.id)


@shared_task(name="Non-Periodic: Make Event from Log")
def makeEventFromLogTask(log_id):
    # get log
    log = Log.objects.get(id=log_id)

    if int(log.status) in (200, 201, 202, 204):
        # make event from log
        # set action
        action = ''
        if log.method == 'POST':
            action = "create"
        if log.method == 'PUT':
            action = "update"
        if log.method == 'PATCH':
            action = "partial_update"
        if log.method == 'DELETE':
            action = "delete"

        # set event object
        event_object = log.path[1:-1]

        # set payload
        event_data = {
            "request": {
                "query": log.request_data['query'],
                "body": log.request_data['body']
            },
            "response": log.response_data['body']
        }

        application = log.application

        # save to db
        event = Event.objects.create(
            application = application,
            action = action,
            event_object = event_object,
            event_data = event_data,

        )
        # call task to process the event.
        postEventToWebhook.apply_async(
            [event.id],
            countdown=0
        )
        return "Event ID: " + str(event.id) +" successfully generated from Log ID: " + str(log.id)

    else:
        return "No event was generated from Log ID: " + str(log.id)