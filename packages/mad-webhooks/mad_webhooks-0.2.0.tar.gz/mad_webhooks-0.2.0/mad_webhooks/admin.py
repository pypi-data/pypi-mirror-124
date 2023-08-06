from mad_webhooks.tasks import postEventToWebhook
from mad_webhooks.models import Event, Log, Webhook, WebhookEventPostAttempt
from django.contrib import admin

# Register your models here.


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
    list_display = ['id', 'application', "endpoint_url", 'is_active', 'created_at']
    raw_id_fields = ['application', ]
    list_filter = ["is_active", "created_at", "updated_at"]



@admin.register(WebhookEventPostAttempt)
class WebhookEventPostAttemptAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
    list_display = ['id', "status", "endpoint_url", 'created_at']
    readonly_fields = list_display + ['response_data', 'event', 'application']
    list_filter = ["status", "created_at", "updated_at"]

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    def post_event_to_webhook(self, request, queryset):
        for obj in queryset:
            postEventToWebhook.apply_async(
            [obj.id],
            countdown=0
        )
    post_event_to_webhook.short_description = "Post the selected event(s) to webhooks"

    ordering = ["-created_at"]
    list_display = ['id', "event_object", "action", "is_processed", 'application', 'created_at']
    readonly_fields = list_display + ['event_data', 'application']
    list_filter = ["action", "is_processed", "created_at", "updated_at"]
    actions = [post_event_to_webhook]

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
    list_display = ['id', "status", "method", "path", 'application', 'created_at']
    raw_id_fields = ['application']
    readonly_fields = list_display + ['request_data', 'response_data', 'user', 'application']
    list_filter = ["status", "method", "created_at", "updated_at"]

    def has_add_permission(self, request, obj=None):
        return False
