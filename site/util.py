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
