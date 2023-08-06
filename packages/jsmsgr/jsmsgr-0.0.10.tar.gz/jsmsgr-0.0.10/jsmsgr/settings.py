"""
Module with settings related to the Semaphore SDK.
"""
from django.conf import settings

# external project configs
JSMSGR_DESTINATION = getattr(settings, "JSMSGR_DESTINATION")

LISTENER_CLIENT_ID = getattr(settings, "LISTENER_CLIENT_ID") if hasattr(settings, "LISTENER_CLIENT_ID") else getattr(settings, "STOMP_LISTENER_CLIENT_ID")

# app configs
SEMAPHORE_SDK_PUBLISHER_NAME = "jsmsgr-publisher"

# replacements
SEMAPHORE_REPLACEMENT_TAG_USER = "###_USER_NAME_###"
