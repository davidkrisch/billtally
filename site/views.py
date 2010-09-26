from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseNotAllowed
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from datetime import date
from models import Bill, Recurrence, BillForm

@login_required
def list_bills(request):
	if request.method not in ['GET']:
		return HttpResponseNotAllowed(['GET'])	

	bills = Bill.objects.filter(user=request.user)
	unpaid = bills.filter(is_paid=False, date__gt=date.today())
	paid = bills.filter(is_paid=True)
	overdue = bills.filter(is_paid=False, date__lte=date.today())
	return render_to_response('list.html', 
			{'unpaid': unpaid, 'paid': paid, 'overdue': overdue},
			context_instance=RequestContext(request))

@login_required
def create_bill(request):
	if request.method not in ('POST', 'GET'):
		return HttpResponseNotAllowed(['GET', 'POST'])

	if request.method == 'GET':
		return render_to_response('bills_form.html', 
				{'form': BillForm()}, context_instance=RequestContext(request))
	else:
		bill_instance = Bill(user=request.user)
		bill = BillForm(request.POST, instance=bill_instance)
		bill.save()
		return redirect('/list/')

#	if request.method == 'GET'
#		render_to_response('create_bill')
#	else:
#		# Save the bill 
#	request
#	return render_to_response(TEMPLATES % 'list.xhtml')
#
#def read_bill(request, bill_id):
#	pass
#
#def update_bill(request, bill_id):
#	pass
#
#def delete_bill(request, bill_id):
#	pass
