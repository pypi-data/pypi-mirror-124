from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from oauth2_provider.settings import oauth2_settings


# Create your models here.


class WebhookAbstract(models.Model):
    application = models.ForeignKey(oauth2_settings.APPLICATION_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Application'))
    endpoint_url = models.CharField(max_length=500, verbose_name=_('Webhook Endpoint'), blank=False, null=False, help_text="Webhook URI - URI where the system will send the payload.")
    query_params = models.JSONField(_('Query Parameters'), default=dict, blank=True, null=True, help_text="These parameters will be sent back to the webhook endpoint via query string.")
    header_params = models.JSONField(_('Header Parameters'), default=dict, blank=True, null=True, help_text="These parameters will be sent back to the webhook endpoint via request header.")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']
        verbose_name = _('Webhook Endpoint')
        verbose_name_plural = _('Webhook Endpoints')

    def __str__(self):
        return "Webhook ID: " + str(self.id)

class Webhook(WebhookAbstract):
    pass

class EventAbstract(models.Model):
    application = models.ForeignKey(oauth2_settings.APPLICATION_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Application'))
    event_object = models.CharField(max_length=500, blank=True, null=True, help_text="")
    action = models.CharField(max_length=50, blank=True, null=True, help_text="create/update/partial-update/delete etc")
    event_data = models.JSONField(_('Event Data'), default=dict, blank=True, null=True, help_text="Payload to be sent to webhook endpoint")
    is_processed = models.BooleanField(default=False, help_text="Whether the event has been posted to webhook endpoints or not")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Event(EventAbstract):
    pass


class WebhookEventPostAttemptAbstract(models.Model):
    application = models.ForeignKey(oauth2_settings.APPLICATION_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Application'))
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Event'))
    endpoint_url = models.CharField(max_length=255, verbose_name=_('Webhook Endpoint'), blank=False, null=False)
    status = models.CharField(_('HTTP Status'), max_length=10, blank=True, null=True)
    response_data = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class WebhookEventPostAttempt(WebhookEventPostAttemptAbstract):
    pass


class LogAbstract(models.Model):
    application = models.ForeignKey(oauth2_settings.APPLICATION_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Created By Application")
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name=_("Users"), help_text="Activity was preformed by this user")
    request_data = models.JSONField(_('Request Data'), default=dict, blank=True, null=True)
    response_data = models.JSONField(_('Response Data'), default=dict, blank=True, null=True)
    path = models.CharField(_('Path'), max_length=500, blank=False, null=False)
    status = models.CharField(_('HTTP Status'), max_length=255, blank=False, null=False)
    method = models.CharField(_('HTTP Method'), max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Log(LogAbstract):
    pass