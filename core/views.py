from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from . import models
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import (
	UserUpdateForm,
	ProfileUpdateForm,
	ApplyLoanForm,
	ModifyLoanForm,
	AcceptLoanForm,
	SalarySlipForm
)

def home(request, page=1):
	loans = []
	# Loans where borrowing user is the current logged in user
	q1 = Q(borrowing_user=request.user)
	# Loans where lending user is not null
	# (Those loans have been accepted by other users)
	q2 = Q(lending_user__isnull=False)
	if request.user.is_authenticated:
		# This is a little complicated
		# We filter rejected loans table where the rejecting user is the
		# current logged in user and create a flat list of loan ids
		# Then we check if loan id of a loan is present in that list
		q3 = Q(loan_id__in=(models.RejectedLoan.objects
			.filter(rejecting_user=request.user)
			.values_list('loan_id', flat=True))
		)

		# Exclude loans which satisfy any of the above queries
		loans = models.Loan.objects.exclude(q1 | q2 | q3)
	else:
		loans = models.Loan.objects.exclude(q2)
	loans = list(reversed(loans))
	paginator = Paginator(loans, per_page=10)
	loans = paginator.get_page(page)
	context = {
		'loans': loans
	}
	return render(request, "home.html", context)

def about(request):
	return render(request, "about.html")

@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		s_form = SalarySlipForm(request.POST, request.FILES)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			slip = s_form.save(commit=False)
			slip.user = request.user
			slip.save()
			messages.success(request, f"Your profile has been updated!")
			return redirect('core:profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
		s_form = SalarySlipForm()

	context = {
		'u_form': u_form,
		'p_form': p_form,
		's_form': s_form
	}

	return render(request, 'profile.html', context)

@login_required
def apply_loan(request):
	if not request.user.profile.first_name:
		messages.error(request, f"Please complete your profile first")
		return redirect('core:profile')
	if request.method=='POST':
		l_form = ApplyLoanForm(request.POST)

		if l_form.is_valid():
			loan = l_form.save(commit=False)
			loan.borrowing_user = request.user
			loan.save()
			messages.success(request, "You've successfully applied for a personal loan!")
			return redirect('core:apply_loan')
	else:
		l_form = ApplyLoanForm()

	context = {
		'l_form': l_form
	}
	return render(request, "apply.html", context)

@login_required
def my_loans(request, page=1):
	loans = models.Loan.objects.filter(borrowing_user=request.user)
	loans = list(reversed(loans))
	paginator = Paginator(loans, per_page=10)
	loans = paginator.get_page(page)
	context = {
		'loans': loans
	}
	return render(request, "my_loans.html", context)

@login_required
def lent_loans(request, page=1):
	loans = models.Loan.objects.filter(lending_user=request.user)
	loans = list(reversed(loans))
	paginator = Paginator(loans, per_page=10)
	loans = paginator.get_page(page)
	context = {
		'loans': loans
	}
	return render(request, "lent_loans.html", context)

@login_required
def my_offers(request, page=1):
	offers = models.ModifiedLoan.objects.filter(borrowing_user=request.user)
	offers = list(reversed(offers))
	paginator = Paginator(offers, per_page=10)
	offers = paginator.get_page(page)
	context = {
		'offers': offers
	}
	return render(request, "my_offers.html", context)

@login_required
def sent_offers(request, page=1):
	offers = models.ModifiedLoan.objects.filter(offering_user=request.user)
	offers = list(reversed(offers))
	paginator = Paginator(offers, per_page=10)
	offers = paginator.get_page(page)
	context = {
		'offers': offers
	}
	return render(request, "sent_offers.html", context)

@login_required
def salary_slips(request):
	slips = models.SalarySlip.objects.filter(user=request.user)
	slips = list(reversed(slips))
	context = {
		'slips': slips
	}
	return render(request, "salary_slips.html", context)

@login_required
def modify_loan(request):
	loan_id = request.GET.get('id')
	if loan_id and loan_id.isdigit():
		if models.ModifiedLoan.objects.filter(loan_id=loan_id).filter(offering_user=request.user):
			messages.success(request, f"You've already modified and offered loan #{loan_id}")
			return redirect('core:home')
		loan = models.Loan.objects.filter(loan_id=loan_id)
		if not loan:
			messages.error(request, f"No loan application with id #{loan_id}")
			return redirect('core:home')
		loan = loan[0]
		l_form = ModifyLoanForm(instance=loan)
		context = {
			'id': loan_id,
			'l_form': l_form
		}
		if request.method=='POST':
			l_form = ModifyLoanForm(request.POST)
			if l_form.is_valid():
				new_tenure = l_form.cleaned_data['tenure']
				new_rate = l_form.cleaned_data['interest_rate']
				if new_tenure == loan.tenure or new_rate == loan.interest_rate:
					messages.error(request, "Please modify one or both of the fields")
					return render(request, "modify_loan.html", context)
				modified_loan = l_form.save(commit=False)
				modified_loan.loan = loan
				modified_loan.offering_user = request.user
				modified_loan.save()
				messages.success(request, "Sent offer for the modified loan")
				return redirect('core:home')
			context['l_form'] = l_form
		return render(request, "modify_loan.html", context)
	messages.error(request, "No valid loan id provided")
	return redirect('core:home')

@login_required
def accept_loan(request):
	loan_id = request.GET.get('id')
	if loan_id and loan_id.isdigit():
		if models.Loan.objects.filter(loan_id=loan_id).filter(lending_user=request.user):
			messages.success(request, f"You've already accepted this loan #{loan_id}")
			return redirect('core:home')
		loan = models.Loan.objects.filter(loan_id=loan_id)
		if not loan:
			messages.error(request, f"No loan application with id #{loan_id}")
			return redirect('core:home')
		loan = loan[0]
		if loan.borrowing_user == request.user:
			messages.error(request, "Cannot accept own loan")
			return redirect('core:home')
		l_form = AcceptLoanForm(instance=loan)
		context = {
			'id': loan_id,
			'l_form': l_form
		}
		if request.method=='POST':
			l_form = AcceptLoanForm(request.POST, instance=loan)
			if l_form.is_valid():
				loan = l_form.save(commit=False)
				loan.lending_user = request.user
				loan.save()
				messages.success(request, "Accepted the loan")
				return redirect('core:home')
			context['l_form'] = l_form
		return render(request, "accept_loan.html", context)
	if not loan_id:
		messages.error(request, "No valid loan id provided")
	if not accepted:
		messages.error(request, "Please confirm accepting the loan")
	return redirect('core:home')

@login_required
def reject_loan(request, loan_id=0):
	loan = models.Loan.objects.filter(loan_id=loan_id)
	if not loan:
		messages.error(request, "No valid loan id provided")
		return redirect('core:home')
	loan = loan[0]
	if loan.borrowing_user == request.user:
		messages.error(request, "Cannot reject own loan application")
		return redirect('core:home')
	rejected_loan = models.RejectedLoan()
	rejected_loan.loan = loan
	rejected_loan.rejecting_user = request.user
	rejected_loan.save()
	messages.info(request, f"Rejected loan #{loan_id}")
	return redirect('core:home')
