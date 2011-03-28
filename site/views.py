from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from models import Bill, Recurrence, RRULE_WEEKDAY_MAP, RECURRENCE_FREQ_MAP
from forms import BillForm, DateRangeForm, RecurFreqForm
from forms import DailyRecurrenceForm, WeeklyRecurrenceForm 
from forms import MonthlyRecurrenceForm, YearlyRecurrenceForm 
from util import get_date_range, date_to_datetime, bill_model_to_forms
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *

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

	bill_list = sorted(bill_list, key=lambda bill: date_to_datetime(bill.date))

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
def delete_bill(request, bill_id):
	'''Delete a bill'''
	if request.method not in ('POST', 'GET'):
		return HttpResponseNotAllowed(['GET', 'POST'])

	bill_obj = get_object_or_404(Bill, pk=bill_id)

	if request.method == 'GET':
		# Show the confirmation page
		return render_to_response('confirm_delete.html', {'bill': bill_obj},
				context_instance=RequestContext(request))
	else:
		name = bill_obj.name
		bill_obj.delete()
		messages.add_message(request, messages.SUCCESS, 'Deleted bill %s' % name)
		return redirect('list_bills')

@login_required
def create_edit_bill(request, bill_id):
	if request.method not in ('POST', 'GET'):
		return HttpResponseNotAllowed(['GET', 'POST'])

	bill_obj = None
	bill_form = recur_freq_form = daily_recurrence_form = None
	weekly_recurrence_form = monthly_recurrence_form = None
	yearly_recurrence_form = None

	if bill_id:
		bill_obj = get_object_or_404(Bill, pk=bill_id)

	if request.method == 'GET':
		# Pass a bunch of unbound forms to the create form
		context = {'bill_form': BillForm(), 
				'recur_freq_form': RecurFreqForm(),
				'daily_recurrence_form': DailyRecurrenceForm(),
				'weekly_recurrence_form': WeeklyRecurrenceForm(),
				'monthly_recurrence_form': MonthlyRecurrenceForm(),
				'yearly_recurrence_form': YearlyRecurrenceForm()}

		if bill_obj:
			context.update(bill_model_to_forms(bill_obj))
	else:
		bill_form = BillForm(request.POST, instance=bill_obj)
		if bill_form.is_valid():
			bill_obj = bill_form.save(commit=False)
			bill_obj.user = request.user
		else:
			# TODO return form errors
			print bill_form.errors

		if 'does_repeat' in bill_form.data:
			frequency_form = RecurFreqForm(request.POST)			
			if frequency_form.is_valid():
				repeats = frequency_form.cleaned_data['repeats']

				recurrence_obj = Recurrence()
				recurrence_obj.dtstart = bill_obj.date

				if repeats == 'monthly':
					monthly_recurrence_form = MonthlyRecurrenceForm(request.POST)
					if monthly_recurrence_form.is_valid():
						recurrence_obj.frequency = 'monthly'
						repeat_by = monthly_recurrence_form.cleaned_data['repeat_by'] 
						repeat_every = monthly_recurrence_form.cleaned_data['repeat_every']

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
					weekly_recurrence_form = WeeklyRecurrenceForm(request.POST) 
					if weekly_recurrence_form.is_valid():
						recurrence_obj.frequency = 'weekly'
						repeat_on = weekly_recurrence_form.cleaned_data['repeat_on'] 
						repeat_every = weekly_recurrence_form.cleaned_data['repeat_every']
						recurrence_obj.byweekday = repeat_on
				elif repeats == 'daily':
					pass
				elif repeats == 'yearly':
					pass
				else:
					# TODO should not get here
					pass

				bill_obj.save()
				recurrence_obj.bill = bill_obj
				recurrence_obj.save()
				return redirect('list_bills')
		else:
			# The bill does not repeat
			bill_obj.save()
			return redirect('list_bills')

	return render_to_response('bills_form.html', context,
				context_instance=RequestContext(request))
