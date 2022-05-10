from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Loan, ModifiedLoan
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, ButtonHolder, Fieldset

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['email']

	def __init__(self, *args, submit_title="Save", **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = [
			'first_name',
			'middle_name',
			'last_name',
			'photo',
			'bank',
			'acc_no',
			'ifsc',
			'ctc',
			'aadhaar_card',
			'pan_card'
		]

	def __init__(self, *args, submit_title="Save", **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.layout = Layout(
			Div(
				Div('first_name', css_class="col-sm-4"),
				Div('middle_name', css_class="col-sm-4"),
				Div('last_name', css_class="col-sm-4"),
				css_class="row"
			),
			Div('photo', css_class="form-control"),
			Div('bank'),
			Div(
				Div('acc_no', css_class="col-sm-6"),
				Div('ifsc', css_class="col-sm-6"),
				css_class="row"
			),
			Div('ctc'),
			Div('aadhaar_card', css_class="form-control"),
			Div('pan_card', css_class="form-control"),
		)

class ApplyLoanForm(forms.ModelForm):
	class Meta:
		model = Loan
		fields = [
			'amount',
			'tenure',
			'interest_rate',
		]
	def __init__(self, *args, submit_title="Apply", **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False

class ModifyLoanForm(forms.ModelForm):
	class Meta:
		model = ModifiedLoan
		fields = [
			'tenure',
			'interest_rate',
		]
	def __init__(self, *args, submit_title="Apply", **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False

class AcceptLoanForm(forms.ModelForm):
	accept = forms.BooleanField()
	class Meta:
		model = Loan
		fields = [
			'amount',
			'tenure',
			'interest_rate',
			'accept'
		]
	def __init__(self, *args, submit_title="Apply", **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = False
		instance = getattr(self, 'instance', None)
		if instance and instance.pk:
			self.fields['amount'].widget.attrs['readonly'] = True
			self.fields['tenure'].widget.attrs['readonly'] = True
			self.fields['interest_rate'].widget.attrs['readonly'] = True
			self.fields['accept'].label = "Accept and provide this loan"
