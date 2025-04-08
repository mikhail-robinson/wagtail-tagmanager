from django import forms
from django.utils.translation import gettext_lazy as _

class MergeTagsForm(forms.Form):
    new_tag_name = forms.CharField(label=_("New tag name"), max_length=255)