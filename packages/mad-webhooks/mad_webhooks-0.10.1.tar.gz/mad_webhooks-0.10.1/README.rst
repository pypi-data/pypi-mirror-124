=====
Mad Webhooks
=====

Mad webooks app for django to webhooks to the user

Quick start
-----------

1. Add "mad_webhooks" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'mad_webhooks',
    ]

2. Include the middlewre at the end in your settings like this::

    MIDDLEWARE = [...
        "mad_webhooks.response.Webhook",
    ]

3. Run ``python manage.py migrate`` to create mad_webhooks models.
