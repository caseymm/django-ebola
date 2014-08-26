from django.shortcuts import render
from django.views import generic

class TemplateView(generic.TemplateView):
    # model = FlatFile
    template = 'templates/home/index.html'
    # context_object_name = 'files'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['sit_reps'] = SitRep.objects.filter()
        return context
    #
    # def get_queryset(self):
    #     """
    #     Returns the contributions related to this committee.
    #     """
    #     files = FlatFile.objects.all().exclude(file_name='bulk_campaign_finance.zip')
    #     return files
