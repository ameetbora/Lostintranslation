from django import forms


choicelist = (
		('1','Monday'),
		('2','Tuesday'),
		('3','Wednesday'),
		('4','Thursday'),
		('5','Friday'),
		('6','Saturday'),
		('7','Sunday'),
	)
class LocationForm(forms.Form):
	lat = forms.FloatField()
	lon = forms.FloatField()
	#day = forms.ChoiceField(choices=choicelist)
	#time = forms.TimeField(widget=forms.TimeInput(format='%H:%M:%S'))
