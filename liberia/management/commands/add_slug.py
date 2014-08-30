from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify

class Command(BaseCommand):
    help = 'Add slug to locations'

    def handle(self, *args, **options):
        for loc in Location.objects.all():
            loc.slug = slugify(loc.name)
            loc.save()
