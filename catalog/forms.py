from django import forms

class RenewBookForm(forms.Form):
	renewal_date = forms.DateField(help_text="Enter a data between now and 4 weeks (default 3).")
