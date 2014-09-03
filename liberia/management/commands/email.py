from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives

class Command(BaseCommand):
    help = 'Send email containing updated data when a new entry is added'

    def handle(self, *args, **options):

        subject, from_email, to = 'UPDATED DATA', 'woot@gmail.com', 'caseymm@gmail.com'
        text_content = 'This is an important message.'
        html_content = '<p>This is an <strong>important</strong> message.</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.attach_file('url_query.json')
        msg.send()
