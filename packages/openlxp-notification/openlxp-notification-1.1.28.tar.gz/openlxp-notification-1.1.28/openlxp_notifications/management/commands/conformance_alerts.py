import logging

from django.core.management.base import BaseCommand

from openlxp_notifications.management.utils.notification import \
    send_notifications, send_notifications_with_msg
from openlxp_notifications.models import (ReceiverEmailConfiguration,
                                          SenderEmailConfiguration,
                                          EmailConfiguration)

logger = logging.getLogger('dict_config_logger')


def send_log_email():
    """ function to send emails of log file to personas"""

    # getting email id to send email to personas

    email_data = ReceiverEmailConfiguration.objects.values_list(
        'email_address',
        flat=True)
    email = list(email_data)
    # Getting sender email id
    sender_email_configuration = SenderEmailConfiguration.objects.first()
    sender = sender_email_configuration.sender_email_address

    email_configuration = EmailConfiguration.objects.values(
        'Subject', 'Logo', 'Banner', 'Email_Content', 'Signature', 'Email_Us',
        'FAQ_URL', 'Unsubscribe_Email_ID', 'Log_path', 'HTML_File').first()
    # SUBJECT = email_configuration.SUBJECT
    # HTML_File = email_configuration.HTML_File
    # LOG_PATH = email_configuration.LOG_PATH
    send_notifications(email, sender, email_configuration)


def send_log_email_with_msg(email, sender, msg):
    """ function to send emails of log file to personas"""

    # Getting sender email id
    send_notifications_with_msg(email, sender, msg)


class Command(BaseCommand):
    """Django command to send an emails to the filer/personas, when the log
    warning/error occurred in the metadata EVTVL process."""

    def handle(self, *args, **options):
        """Email log notification is sent to filer/personas when warning/error
        occurred in EVTVL process"""
        send_log_email()
