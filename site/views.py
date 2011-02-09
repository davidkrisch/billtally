from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseNotAllowed
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from datetime import date
from models import Bill, Recurrence, RRULE_WEEKDAY_MAP
from forms import BillForm, RecurrenceForm, DateRangeForm
from util import get_date_range
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *

def api_create_bill(request):
	"""Create a Bill and the corresponding Recurrance if necessary

	Throws a FormErrorException if there is a validation error

	Parameters:
		request - HttpRequest
	"""
	pass

@login_required
def list_bills(request):
	'''Display the users list of bills
	
		Displays bills for the next 30 days by default

		Parameters (optional)
			start - the first date to display bills for
			end - the last date to display bills for
	'''
	if request.method not in ['GET']:
		return HttpResponseNotAllowed(['GET'])	

	start = end = None

	date_range_form = DateRangeForm(request.GET)
	if date_range_form.is_valid():
		start_date = date_range_form.cleaned_data['start']
		end_date = date_range_form.cleaned_data['end']
		start, end = get_date_range(start=start_date, end=end_date)

		# TODO create a unit test for this
		next_start, next_end = get_date_range(start=end+relativedelta(days=+1)) 
		prev_start, prev_end = get_date_range(end=start+relativedelta(days=-1)) 
	else:
		pass
		# TODO return validation error

	bill_list = []

	recurrences = Recurrence.objects.filter(bill__user=request.user)
	for recurrence in recurrences:
		occurrences = recurrence.as_list(start_date=start, end_date=end)
		for date in occurrences:
			to_add = recurrence.bill
			to_add.date = date
			bill_list.append(to_add)

	bills = Bill.objects.filter(user=request.user). \
									filter(date__gte=start, date__lte=end)
	for bill in bills:
		if not bill_in_list(bill_list, bill):
			bill_list.append(bill)

	return render_to_response('list.html', 
			{'bill_list': bill_list, 'start_date': start, 'end_date': end,
			 'next_start': next_start, 'next_end': next_end, 
			 'prev_start': prev_start, 'prev_end': prev_end},
			context_instance=RequestContext(request))

def bill_in_list(list, bill):
	'''Return True if bill is in list, false otherwise'''
	for b in list:
		if b.id == bill.id:
			return True
	return False

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
				recurrence_obj = Recurrence(bill=bill_obj)
				recurrence_obj.dtstart = bill_obj.date
				repeats = recurrence_form.cleaned_data['repeats']
				if repeats == 'monthly':
					recurrence_obj.frequency = 'monthly'
					repeat_by = recurrence_form.cleaned_data['repeat_by'] 
					repeat_every = recurrence_form.cleaned_data['repeat_every']

					if repeat_by == 'day_of_month':
						recurrence_obj.repeat_every = repeat_every
						recurrence_obj.bymonthday = bill_obj.date.day
					elif repeat_by == 'day_of_week':
						# 'Monthly on the third Friday'
						temp = recurrence_obj.dtstart
						i = 0
						while temp.month == recurrence_obj.dtstart.month:
							temp = temp + relativedelta(weeks=-1)
							i += 1
						weekday = recurrence_obj.dtstart.weekday()
						recurrence_obj.byweekday = [weekday]
						recurrence_obj.byweekdaycount = i
				elif repeats == 'weekly':
					recurrence_obj.frequency = 'weekly'
					repeat_on = recurrence_form.cleaned_data['repeat_on'] 
					repeat_every = recurrence_form.cleaned_data['repeat_every']
					recurrence_obj.byweekday = repeat_on
				elif repeats == 'daily':
					pass
				elif repeats == 'yearly':
					pass
				else:
					# TODO should not get here
					pass

				has_end = recurrence_form.cleaned_data['has_end']
				if has_end:
					end_date = recurrence_form.cleaned_data['end_date']
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
