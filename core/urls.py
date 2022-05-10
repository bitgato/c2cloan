from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

app_name = 'core'

urlpatterns = [
	path('', views.home, name='home'),
	path('<int:page>', views.home, name='home_page'),
	path('about', views.about, name='about'),
	path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
	path('accounts/profile/', views.profile, name='profile'),
	path('accounts/profile/apply/', views.apply_loan, name='apply_loan'),
	path('accounts/profile/my-loans', views.my_loans, name='my_loans'),
	path('accounts/profile/my-loans/<int:page>', views.my_loans, name='my_loans_page'),
	path('accounts/profile/lent-loans', views.lent_loans, name='lent_loans'),
	path('accounts/profile/lent-loans/<int:page>', views.lent_loans, name='lent_loans_page'),
	path('accounts/profile/my-offers', views.my_offers, name='my_offers'),
	path('accounts/profile/my-offers/<int:page>', views.my_offers, name='my_offers_page'),
	path('accounts/profile/sent-offers', views.sent_offers, name='sent_offers'),
	path('accounts/profile/sent-offers/<int:page>', views.sent_offers, name='sent_offers_page'),
	path('accounts/profile/salary-slips/', views.salary_slips, name='salary_slips'),
	path('modify-loan/', views.modify_loan, name='modify_loan'),
	path('accept-loan/', views.accept_loan, name='accept_loan'),
	path('reject-loan/', views.reject_loan, name='reject_loan'),
	path('reject-loan/<int:loan_id>', views.reject_loan, name='reject_loan'),
]
