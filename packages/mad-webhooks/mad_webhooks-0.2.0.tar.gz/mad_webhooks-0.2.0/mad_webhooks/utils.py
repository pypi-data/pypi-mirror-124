from os.path import splitext, basename, join
import uuid
import random
import string
import re
import requests
import json
from django.http import Http404
from django.contrib.auth.hashers import make_password
from random import randint
from django.conf import settings
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.models import get_access_token_model
from mad_webhooks.models import Log, WebhookEventPostAttempt
from rest_framework.authentication import get_authorization_header


def randomString(stringLength=8):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))



def getTokenUser(access_token, application):
    if access_token is None:
        user = None
    elif application.authorization_grant_type == 'client-credentials':
        user = None
    else:
        user = access_token.user

    return user



def getAccessToken(request):
    try:
        # return a valid authorization token from request
        return get_authorization_header(request).split()[-1].decode('UTF-8')
    except IndexError as error:
        raise Http404


def getAccessTokenDetails(token):
    try:
        d = get_access_token_model().objects.get(token=token)
        return d
    except get_access_token_model().DoesNotExist:
        return None


def getApplicationDataFromRequest(request):

    try:
        # return a valid authorization token from request
        get_authorization_header(request).split()[-1].decode('UTF-8')

        access_token = getAccessTokenDetails( getAccessToken(request) )
        user = getTokenUser(access_token, access_token.application)

        application_data = {
            "access_token": access_token,
            "application": access_token.application,
            # this is the authorized user who used his user/pass with some client_id/client_secret to access the application
            "token_user": user,
        }
        return application_data

    except IndexError as error:

        application_data = {
            "access_token": None,
            "application": None,
            "token_user": None,
        }

        return application_data

    except AttributeError as ae:
        application_data = {
            "access_token": None,
            "application": None,
            "token_user": None,
        }

        return application_data




def createLog(status_code, method, path, request_data, response_data, application = None, user = None):
    if application is not None:
        application = oauth2_settings.APPLICATION_MODEL.objects.get(id=application)

    log = Log.objects.create(
        status = status_code,
        method = method,
        path = path,
        request_data = request_data,
        response_data = response_data,
        application = application,
        user = user
    )
    return log


def postEventToWebhooks(event, webhooks):
    # event = Event.objects.get(id=event.id)
    # for each endpoint send the event to the webhook via POST
    for webhook in webhooks:
        # make query
        query_params = webhook.query_params

        headers = {
            "User-Agent": settings.SITE_TITLE+"/"+settings.CURRENT_VERSION
        }
        if webhook.header_params is not None:
            header_params = webhook.header_params
            headers.update(header_params)
        # make payload
        payload = {
            "object": event.event_object,
            "action": event.action,
            "data": str(json.dumps(event.event_data)),
        }

        try:
            # send event.data to the webhook endpoint
            send = requests.post(
                webhook.endpoint_url,
                data=payload,
                params=query_params,
                headers=headers
            )
            r = {
                'status_code': send.status_code,
                'text': send.text
            }
        except requests.RequestException as err:
            r = {
                'status_code': None,
                'text': err
            }
        except requests.ConnectionError as err:
            r = {
                'status_code': None,
                'text': err
            }
        except requests.HTTPError as err:
            r = {
                'status_code': None,
                'text': err
            }
        except requests.URLRequired as err:
            r = {
                'status_code': None,
                'text': err
            }
        except requests.TooManyRedirects as err:
            r = {
                'status_code': None,
                'text': err
            }
        except requests.ConnectTimeout as err:
            r = {
                'status_code': None,
                'text': err
            }
        except requests.ReadTimeout as err:
            r = {
                'status_code': None,
                'text': err
            }
        except requests.Timeout as err:
            r = {
                'status_code': None,
                'text': err
            }

        save_response = WebhookEventPostAttempt.objects.create(
            application = event.application,
            event = event,
            endpoint_url = str(webhook.endpoint_url),
            status = r['status_code'],
            response_data = r['text'],
        )

    event.is_processed = True
    event.save()
