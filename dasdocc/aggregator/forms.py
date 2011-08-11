from django import forms
from dasdocc.aggregator.models import StaticContent

class StaticContentForm(forms.ModelForm):

	class Meta:
		model = StaticContent

