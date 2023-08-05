from django.contrib import admin

from .models import ReceiverEmailConfiguration, SenderEmailConfiguration, \
    EmailConfiguration


@admin.register(ReceiverEmailConfiguration)
class ReceiverEmailConfigurationAdmin(admin.ModelAdmin):
    list_display = ('email_address',)


@admin.register(SenderEmailConfiguration)
class SenderEmailConfigurationAdmin(admin.ModelAdmin):
    list_display = ('sender_email_address',)


@admin.register(EmailConfiguration)
class EmailConfigurationAdmin(admin.ModelAdmin):
    list_display = ('Subject',
                    'Logo',
                    'Banner',
                    'Log_path',
                    'Email_Content',
                    'HTML_File',)
