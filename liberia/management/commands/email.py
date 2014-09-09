from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Send email containing updated data when a new entry is added'

    def handle(self, *args, **options):
        # today = datetime.today().strftime("%m-%d-%Y")
        latest_date = SitRep.objects.latest('formatted_date')
        latest_str = str(latest_date.formatted_date)
        subject, from_email, to = 'UPDATED DATA '+latest_str, 'unc.crisis.team@gmail.com', 'stking@email.unc.edu'
        text_content = 'This is contains SitRep data through '+latest_str+'.'
        # html_content = '<p>This is an <strong>important</strong> message.</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        msg.attach_file('latest_'+latest_str+'.zip')
        msg.send()
