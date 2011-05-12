from django import forms
from aggregator.models import StaticContent

class StaticContentForm(forms.ModelForm):

	class Meta:
		model = StaticContent

