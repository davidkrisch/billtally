from datetime import datetime, time
from dateutil.relativedelta import relativedelta

def get_date_range(start=None, end=None, obj=None):
	'''Gets a start date and and end date

		Parameters
			start - (datetime) 
			end - (datetime) 
	'''
	if not start:
		if end:
			start = end + relativedelta(months=-1)
		else:
			start = datetime.today()

	if not end:
		end = start + relativedelta(months=+1)
		end = datetime.combine(end, time())

	return (start, end)


def date_to_datetime(date):
	'''Converts a date object to a datetime object with a time of midnight'''
	return datetime.combine(date, time())

def bill_model_to_forms(bill_model):
	'''Converts a bill model to form objects suitable for display'''
	from forms import BillForm, RecurFreqForm, DailyRecurrenceForm, WeeklyRecurrenceForm, \
			MonthlyRecurrenceForm, YearlyRecurrenceForm

	forms = {}
	recurrence = bill_model.get_recurrence()

	if recurrence:
		forms['bill_form'] = BillForm(initial={'does_repeat': True}, instance=bill_model)	
		forms['recur_freq_form'] = RecurFreqForm({'repeats': recurrence.frequency})
		if recurrence.frequency == 'daily':
			forms['daily_recurrence_form'] = DailyRecurrenceForm()
		elif recurrence.frequency == 'weekly':
			forms['weekly_recurrence_form'] = WeeklyRecurrenceForm(initial={'repeat_on': recurrence.byweekday})
		elif recurrence.frequency == 'monthly':
			repeat_by = None
			if recurrence.bymonthday:
				repeat_by = 'day_of_month'
			else:
				repeat_by = 'day_of_week'

			forms['monthly_recurrence_form'] = \
					MonthlyRecurrenceForm(initial={'repeat_every_monthly': recurrence.interval, 'repeat_by': repeat_by})
		elif recurrence.frequency == 'yearly':
			forms['yearly_recurrence_form'] = YearlyRecurrenceForm()
	else:
		forms['bill_form'] = BillForm(instance=bill_model)	


	return forms

