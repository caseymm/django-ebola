from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='Must be a SitRep with .xls ending.'
    )
    sit_rep_date = forms.CharField(
        label='Enter date with yyyy-mm-dd format',
        help_text='For example, September 17th, 2014 would be formatted as 2014-09-17'
        )
    month_format = forms.CharField(
        label='Enter month format with punctuation.',
        help_text='ex) "Aug" or "Sept." Do not include the quotation marks.'
        )
