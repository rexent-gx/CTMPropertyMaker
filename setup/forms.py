from django import forms
from django.forms.fields import ChoiceField, MultipleChoiceField
from django.forms.widgets import Select, CheckboxSelectMultiple

METHODS = (
	('fixed','fixed'),
	('random','random'),
	('repeat','repeat'),
	('top','top'),
	('vertical','vertical'),
	('horizontal','horizontal'),
	('horizontal+vertical','horizontal+vertical'),
	('vertical+horizontal','vertical+horizontal'),
	('ctm','ctm'),
	)

TorF = (
	('true','True'),
	('false','False'),
	)

SYMMETRY = (
	('none','none'),
	('opposite','opposite'),
	('all','all'),
	)

RSYMMETRY = (
	('none','none'),
	('opposite','opposite'),
	)

FACES = (
	('','(none)'),
	('bottom','bottom'),
	('top','top'),
	('north','north'),
	('south','south'),
	('east','east'),
	('west','west'),
	('sides','sides'),
	('all','all'),
	)

CONNECT = (
	('','(none)'),
	('block','block'),
	('tile','tile'),
	('material','material'),
	)

RENDERPASS = (
	('','(none)'),
	('0','0'),
	('1','1'),
	('2','2'),
	('3','3'),
	)

JADOUNUMS = [
	('2','2'),
	('3','3'),
	('5','5'),
	('7','7'),
	]

class SetupForm(forms.Form):
	file_name = forms.CharField()
	tiles = forms.CharField(required=False)

class MethodForm(forms.Form):
	method = ChoiceField(widget=Select(attrs={'onchange' : "MethodChange();",}), choices=METHODS)

class RandomForm(forms.Form):
	weight = forms.CharField(required=False)
	linked = ChoiceField(widget=Select, choices=TorF)
	symmetry = ChoiceField(widget=Select, choices=SYMMETRY)

class RepeatForm(forms.Form):
	width = forms.CharField(required=False)
	height = forms.CharField(required=False)
	rsymmetry = ChoiceField(widget=Select, choices=RSYMMETRY, label='Symmetry')

class JadouNums(forms.Form):
	jnums = MultipleChoiceField(widget=CheckboxSelectMultiple(), choices=JADOUNUMS)

class OptionalForm(forms.Form):
	source = forms.CharField(required=False)
	metadata = forms.CharField(required=False)
	faces = ChoiceField(widget=Select, choices=FACES, required=False)
	matchtiles = forms.CharField(required=False)
	biomes = forms.CharField(required=False)
	minheight = forms.CharField(required=False)
	maxheight = forms.CharField(required=False)
	matchblocks = forms.CharField(required=False)
	connect = ChoiceField(widget=Select, choices=CONNECT, required=False)
	renderpass = ChoiceField(widget=Select, choices=RENDERPASS, required=False)