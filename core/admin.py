from django.contrib import admin
# from .models import Borrowing_Loan, Lending_Loan, Profile
from .models import (
	Loan,
	ModifiedLoan,
	RejectedLoan,
	SalarySlip,
	Profile
)

# admin.site.register(Borrowing_Loan)
# admin.site.register(Lending_Loan)
# admin.site.register(Profile)
admin.site.register(Loan)
admin.site.register(ModifiedLoan)
admin.site.register(RejectedLoan)
admin.site.register(SalarySlip)
admin.site.register(Profile)