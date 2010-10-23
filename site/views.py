from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseNotAllowed
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from datetime import date
from models import Bill, Recurrence, RECURRENCE_FREQ_MAP
from forms import BillForm, RecurrenceForm

def api_create_bill(request):
	"""Create a Bill and the corresponding Recurrance if necessary

	Throws a FormErrorException if there is a validation error

	Parameters:
		request - HttpRequest
	"""
	pass

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

	bill_obj = None

	if request.method == 'GET':
		return render_to_response('bills_form.html', 
				{'bill_form': BillForm(), 'recurrence_form': RecurrenceForm()},
				 context_instance=RequestContext(request))
	else:
		bill_form = BillForm(request.POST)
		if bill_form.is_valid():
			bill_obj = bill_form.save(commit=False)
			bill_obj.user = request.user
		else:
			# TODO return form errors
			print bill_form.errors

		if 'does_repeat' in bill_form.data:
			recurrence_form = RecurrenceForm(request.POST)
			if recurrence_form.is_valid():
				bill_obj.save()
				repeats = recurrence_form.cleaned_data['repeats']
				if repeats == 'monthly':
					repeat_by = recurrence_form.cleaned_data['repeat_by'] 
					repeat_every = recurrence_form.cleaned_data['repeat_every']
					has_end = recurrence_form.cleaned_data['has_end']
					end_date = recurrence_form.cleaned_data['end_date']

					recurrence_obj = Recurrence(bill=bill_obj)
					recurrence_obj.frequency = RECURRENCE_FREQ_MAP['monthly']
					recurrence_obj.dtstart = bill_obj.date

					if repeat_by == 'day_of_month':
						recurrence_obj.bymonthday = repeat_every
					else:
						pass
						# TODO 'Monthly on the third Friday'

					if has_end:
						recurrence_obj.until = end_date

					recurrence_obj.save()
			else:
				# TODO return form errors
				print recurrence_form.errors
		else:
			# The bill does not repeat
			bill_obj.save()

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
