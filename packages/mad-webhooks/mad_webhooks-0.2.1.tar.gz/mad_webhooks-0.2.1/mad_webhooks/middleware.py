from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from rest_framework.response import Response
import json

from mad_webhooks.models import Log
from mad_webhooks.utils import getApplicationDataFromRequest
# from django.conf import settings
class Webhook:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        # settings.OAUTH2_PROVIDER['PKCE_REQUIRED'] = enforce_public

        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        # skip admin
        if "api." in request.META['HTTP_HOST']:
            if request.method not in ('GET', 'HEAD', 'OPTIONS') and response.status_code not in (404, 500, 501):
                # get application detail
                app_data = getApplicationDataFromRequest(request)

                user = app_data['token_user']

                # prepare request data
                request_data = {
                    # "header": request.META,
                    "query": request.GET,
                    "body": request.POST,
                }

                if request.method == "DELETE":
                    response_body = ""
                else:
                    response_body = json.loads(response.render().content)

                # prepare response data
                response_data = {
                    "body":response_body,
                }


                # log data to db
                log = Log.objects.create(
                    status = response.status_code,
                    method = request.method,
                    path = request.path,
                    request_data = request_data,
                    response_data = response_data,
                    application = app_data['application'],
                    user = user
                )

        # # experiments
        # if isinstance(response, HttpResponse):
        #     response.data['webhook_data'] = reverse('admin:index', host='admin')
        #     # you need to change private attribute `_is_render`
        #     # to call render second time
        #     response._is_rendered = False
        #     response.render()




        return response
