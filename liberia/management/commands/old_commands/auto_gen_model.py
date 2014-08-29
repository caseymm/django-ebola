import re
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = """

    Generate genereic field info for attributes in a dictionary.
    This mostly stemmed from lack of desire to copy and paste.

    """

    def handle(self, *args, **options):

        print "This is just to create generic text for a model."
        print "You will need to adjust if using class based views, and if using anything other than character or text fields."

        model_name = raw_input ("Model name: ")
        print
        print
        print "Please enter 'text' or 'char' depending on what you would like to use as the default field format."


        field_type = raw_input ("Field Type: ")
        while field_type != 'text' and field_type != 'char':
            print
            print "Please type either 'text' or 'char'"
            field_type = raw_input ("Field type: ")

        if field_type == 'char':
            print 'Default CharField length? (please type and integer).'
            ml = raw_input ("CharacterField length: ")
            field_len = re.search(r'^[0-9]+', ml)
            while bool(field_len) == False:
                print 'Please type an integer.'
                ml = raw_input ("CharacterField length: ")
                field_len = re.search(r'^[0-9]+', ml)


            gen_char = "= models.CharField(max_length="+ml+", blank=True)"
        gen_text = "= models.TextField(blank=True)"

        print
        print
        print 'Please enter your list as a comma separated string (no brackets).'
        attr_list_str = raw_input ("enter list: ")
        split_string = attr_list_str.replace("'", "").split(',')
        attr_list = []
        for attr in split_string:
            sa = attr.strip()
            attr_list.append(sa)

        print
        print
        print "class "+model_name+"(models.Model):"
        for attr_name in attr_list:
            if field_type == 'char':
                print "    "+attr_name, gen_char
            else:
                print "    "+attr_name, gen_text
