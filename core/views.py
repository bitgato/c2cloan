from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, ApplyLoanForm, ModifyLoanForm

def home(request):
	if request.user.is_authenticated:
		context = {
			'loans': models.Loan.objects.exclude(borrowing_user=request.user)
		}
	else:
		context = {
			'loans': models.Loan.objects.all()
		}
	return render(request, "home.html", context)

@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f"Your profile has been updated!")
			return redirect('core:profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form': u_form,
		'p_form': p_form
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
def my_loans(request):
	context = {
		'loans': models.Loan.objects.filter(borrowing_user=request.user)
	}
	return render(request, "my_loans.html", context)

@login_required
def my_offers(request):
	context = {
		'offers': models.ModifiedLoan.objects.filter(borrowing_user=request.user)
	}
	return render(request, "my_offers.html", context)

@login_required
def sent_offers(request):
	context = {
		'offers': models.ModifiedLoan.objects.filter(offering_user=request.user)
	}
	return render(request, "sent_offers.html", context)

@login_required
def modify_loan(request):
	loan_id = request.GET.get('id')
	if loan_id:
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
			else:
				context['l_form'] = l_form
		return render(request, "modify_loan.html", context)
	else:
		messages.error(request, "No valid loan id provided")
		return redirect('core:home')
