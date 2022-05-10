from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import re
from PIL import Image

def bank_acc_no(value):
	if value is not None and value.isdigit()==False:
		raise ValidationError('Invalid bank account number')

def ifsc(value):
	regex = "^[A-Z]{4}0[A-Z0-9]{6}$"
	p = re.compile(regex)
	if not re.search(p, value):
		raise ValidationError('Invalid IFSC code')

def interest_rate(value):
	if value < 0:
		raise ValidationError('Interest rate should be greater than 0')

class Loan(models.Model):
	loan_id = models.BigAutoField(primary_key=True)

	borrowing_user = models.ForeignKey(User, related_name='%(class)s_borrowing', on_delete=models.CASCADE)
	lending_user = models.ForeignKey(User, related_name='%(class)s_lending', null=True, on_delete=models.CASCADE)

	amount = models.PositiveIntegerField('Amount required')
	tenure = models.PositiveIntegerField('Tenure (in months)', validators=[MinValueValidator(1)])
	interest_rate = models.FloatField('Interest rate', validators=[interest_rate])

	date_applied = models.DateField(auto_now_add=True)

	date_borrowing_start = models.DateField(null=True)
	date_lending_end = models.DateField(null=True)

	def __str__(self):
		return "loan #"+str(self.loan_id)

class ModifiedLoan(models.Model):
	offer_id = models.BigAutoField(primary_key=True)
	loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
	tenure = models.PositiveIntegerField('New Tenure (in months)', validators=[MinValueValidator(1)])
	interest_rate = models.FloatField('New Interest rate', validators=[interest_rate])
	borrowing_user = models.ForeignKey(User, related_name='%(class)s_borrowing', on_delete=models.CASCADE)
	offering_user = models.ForeignKey(User, related_name='%(class)s_offering', null=True, on_delete=models.CASCADE)

class Profile(models.Model):
	profile_id = models.BigAutoField(primary_key=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	first_name = models.CharField('First Name', max_length=50)
	middle_name = models.CharField('Middle Name', max_length=50, blank=True, null=True)
	last_name = models.CharField('Last Name', max_length=50)
	photo = models.ImageField('Profile picture', default='default.jpg', upload_to='photo')

	bank = models.CharField('Bank name', max_length=100)
	acc_no = models.CharField('Account Number', max_length=40, validators=[bank_acc_no], null=True)
	ifsc = models.CharField('IFSC Code', max_length=11, validators=[ifsc])

	ctc = models.PositiveIntegerField('CTC', null=True)

	aadhaar_card = models.FileField('Aadhaar card', upload_to='aadhaar_card', blank=True)
	pan_card = models.FileField('Pan card', upload_to='pan_card', blank=True)

	cibil_score = models.IntegerField('Cibil score', null=True)

	def __str__(self):
		return f"{self.user.username} Profile"

	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)
		photo = Image.open(self.photo.path)

		if photo.height > 300 or photo.width > 300:
			output_size = (300, 300)
			photo.thumbnail(output_size)
			photo.save(self.photo.path)

