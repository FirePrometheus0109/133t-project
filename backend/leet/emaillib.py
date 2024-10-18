# pylint: disable=too-many-arguments
import yaml

from django.core import mail
from django.template.loader import get_template


def prepare_message(template_name, to, context, charset, cc, bcc):
    template = get_template(template_name).render(context)
    template_dict = yaml.safe_load(template)
    if not isinstance(to, list):
        to = [to]
    message = mail.EmailMessage(
        subject=template_dict['subject'][:-1],  # [:-1] drop '\n' after load
        body=template_dict['body'],
        to=to,
        cc=cc,
        bcc=bcc)
    message.content_subtype = template_dict['content_type']
    message.encoding = charset
    return message


def send_email(template_name, to, context, charset=None, cc=None, bcc=None):
    """
    Send email from server
    :param template_name: name of template for email
    :param to: list of emails
    :param context: variables for template
    :param charset: if 'None' charset is using default charset
    :param cc: list of emails
    :param bcc: list of emails
    """
    message = prepare_message(template_name, to, context, charset, cc, bcc)
    return message.send(fail_silently=True)


def send_emails(template_name, context_list, charset=None, cc=None, bcc=None):
    """
    Send multiple emails with the same template
    :param template_name: name of template for email
    :param context_list: list of contexts, should contain user
    :param charset: if 'None' charset is using default charset
    :param cc: list of emails
    :param bcc: list of emails
    """
    to_list = [c['user'].email for c in context_list]
    emails = []
    for to, context in zip(to_list, context_list):
        message = prepare_message(
            template_name, to, context, charset, cc, bcc)
        emails.append(message)
    with mail.get_connection(fail_silently=True) as connection:
        connection.send_messages(emails)


def send_user_generated_email(
        subject, template_name, to, context, charset=None, cc=None, bcc=None):
    """
    Send email from server
    :param subject: subject for email
    :param template_name: name of template for email
    :param to: list of emails
    :param context: variables for template
    :param charset: if 'None' charset is using default charset
    :param cc: list of emails
    :param bcc: list of emails
    """
    body = get_template(template_name).render(context)
    if not isinstance(to, list):
        to = [to]
    message = mail.EmailMessage(
        subject=subject,
        body=body,
        to=to,
        cc=cc,
        bcc=bcc)
    message.content_subtype = 'html'
    message.encoding = charset
    return message.send(fail_silently=True)
