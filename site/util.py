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
	from forms import BillForm
	from models import Recurrence

	forms = {}
	forms['bill_form'] = BillForm(instance=bill_model)	
	recurrence = bill_model.get_recurrence()
	if recurrence:
		if recurrence.frequency == 'monthly':
			print 'monthly'

	return forms

