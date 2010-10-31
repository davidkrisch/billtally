from datetime import datetime, time
from dateutil.relativedelta import relativedelta

def get_date_range(start, end):
		if not start:
			start = datetime.today()
		if not end:
			end = start + relativedelta(months=+1)
			end = datetime.combine(end, time())
		return (start, end)
