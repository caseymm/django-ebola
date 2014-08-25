from django.shortcuts import render
from django.views import generic

class TemplateView(generic.TemplateView):
    # model = FlatFile
    template = 'templates/home/index.html'
    # context_object_name = 'files'

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super(IndexView, self).get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['bulk_download'] = FlatFile.objects.filter(
    #         file_name='bulk_campaign_finance.zip')
    #     return context
    #
    # def get_queryset(self):
    #     """
    #     Returns the contributions related to this committee.
    #     """
    #     files = FlatFile.objects.all().exclude(file_name='bulk_campaign_finance.zip')
    #     return files
