from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

app_name = 'core'

urlpatterns = [
	path('', views.home, name='home'),
	path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
	path('accounts/profile/', views.profile, name='profile'),
	path('accounts/profile/apply/', views.apply_loan, name='apply_loan'),
	path('accounts/profile/my-loans', views.my_loans, name='my_loans'),
	path('accounts/profile/my-offers', views.my_offers, name='my_offers'),
	path('accounts/profile/sent-offers', views.sent_offers, name='sent_offers'),
	path('modify-loan/', views.modify_loan, name='modify_loan'),
	path('accept-loan/', views.accept_loan, name='accept_loan'),
]
