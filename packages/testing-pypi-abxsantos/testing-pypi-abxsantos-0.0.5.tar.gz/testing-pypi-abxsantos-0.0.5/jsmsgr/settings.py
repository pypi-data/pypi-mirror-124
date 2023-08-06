"""
Module with settings related to the Semaphore SDK.
"""
from django.conf import settings

# external project configs
JSMSGR_DESTINATION = getattr(settings, "JSMSGR_DESTINATION")
USER_API_HOST = getattr(settings, "USER_API_HOST")
STOMP_SERVER_HOST = getattr(settings, "STOMP_SERVER_HOST")
STOMP_SERVER_PORT = getattr(settings, "STOMP_SERVER_PORT")
STOMP_SERVER_USER = getattr(settings, "STOMP_SERVER_USER")
STOMP_SERVER_PASSWORD = getattr(settings, "STOMP_SERVER_PASSWORD")
STOMP_USE_SSL = getattr(settings, "STOMP_USE_SSL")
LISTENER_CLIENT_ID = getattr(settings, "LISTENER_CLIENT_ID") if hasattr(settings, "LISTENER_CLIENT_ID") else getattr(settings, "STOMP_LISTENER_CLIENT_ID")


# app configs
SEMAPHORE_SDK_PUBLISHER_NAME = "jsmsgr-publisher"

# replacements
SEMAPHORE_REPLACEMENT_TAG_USER = "###_USER_NAME_###"
