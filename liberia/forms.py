from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='Must be a SitRep with .xls ending.'
    )
