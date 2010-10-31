from django.test import TestCase, Client
from billtally.site.models import Bill, Recurrence
from django.contrib.auth.models import User
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal

def get_date(date_str):
	return datetime.strptime(date_str, '%Y-%m-%d').date()

class BillModelTest(TestCase):
	'''Test the Bill model'''
	fixtures = ['single_user.json']

	def setUp(self):
		'''Set up some test data'''
		self.bill_data = {'user': User.objects.get(pk=1), 'name': 'David Krisch', 'amount': '12.45',
				'date': '2010-10-01', 'is_paid': True}
		self.recurrence_data = {'frequency': 'monthly', 'dtstart': '2010-10-01'}

	def test_create_simple_bill(self):
		'''Test creating a simple bill'''
		bill = Bill(**self.bill_data)
		bill.save()
		self.assertTrue(Bill.objects.count(), 1)

	def test_create_recurring_bill(self):
		'''Test creating a recurring bill'''
		bill = Bill(**self.bill_data)
		bill.save()
		recurrence = Recurrence(**self.recurrence_data)
		recurrence.bill = bill
		recurrence.save()
		start = datetime(2030, 12, 15)
		self.assertTrue(Bill.objects.count(), 1)
		self.assertTrue(bill.recurrence_set.count(), 1)

	def test_as_list(self):
		'''Test the Bill Model's as_rrule method'''
		bill = Bill(**self.bill_data)
		bill.save()
		recurrence = Recurrence(**self.recurrence_data)
		recurrence.bill = bill
		recurrence.save()
		recurrence = Recurrence.objects.all()[0]
		r_list = recurrence.as_list()
		self.assertEquals(len(r_list), 1)  

		# The next due date should be the first day of next month
		expected = datetime.today() + relativedelta(day=1, months=+1)
		self.assertEquals(r_list[0].date(), expected.date())

	def test_as_list_with_until_set(self):
		'''Test as_list with an until set in recurrence'''
		bill = Bill(**self.bill_data)
		bill.save()
		self.recurrence_data['until'] = '2010-11-30'
		recurrence = Recurrence(**self.recurrence_data)
		recurrence.bill = bill
		recurrence.save()
		recurrence = Recurrence.objects.all()[0]
		r_list = recurrence.as_list(start_date=datetime(2010, 10, 15))
		self.assertEquals(len(r_list), 1)  

		# The next due date should be the first day of next month
		self.assertEquals(r_list[0], datetime(2010, 11, 1))


	def test_as_list_with_startdate(self):
		'''Test as_list with a start date'''
		bill = Bill(**self.bill_data)
		bill.save()
		recurrence = Recurrence(**self.recurrence_data)
		recurrence.bill = bill
		recurrence.save()
		recurrence = Recurrence.objects.all()[0]
		start = datetime(2030, 12, 15)
		r_list = recurrence.as_list(start_date=start)
		expected = start + relativedelta(day=1, months=+1)
		self.assertEquals(r_list[0].date(), expected.date())

	def test_as_list_with_startdate_and_enddate(self):
		'''Test as_list with a end date'''
		bill = Bill(**self.bill_data)
		bill.save()
		recurrence = Recurrence(**self.recurrence_data)
		recurrence.bill = bill
		recurrence.save()
		recurrence = Recurrence.objects.all()[0]
		start = datetime(2030, 12, 15)
		start = datetime(2010, 11, 15)
		end = datetime(2010, 12, 15)
		r_list = recurrence.as_list(start_date=start, end_date=end)
		self.assertEquals(len(r_list), 1)
		self.assertEquals(r_list[0].date(), datetime(2010, 12, 1).date())

class BillViewTest(TestCase):
	fixtures = ['users.json', 'bills.json']

	def setUp(self):
		'''Set User passwords and log one in'''
		for user in User.objects.all():
			user.set_password('password')
			user.save()
		self.client.login(username='davidkrisch', password='password')

	def test_bill_list(self):
		"""Test that the list_bills view returns a list of bills"""
		response = self.client.get('/list/', follow=True)
		self.failUnlessEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'list.html')
		self.assertTrue(len(response.context['unpaid']) == 1)
		self.assertTrue(len(response.context['paid']) == 2)
		self.assertTrue(len(response.context['overdue']) == 1)

class CreateBillTest(TestCase):
	fixtures = ['users.json']

	def setUp(self):
		'''Set User passwords and log one in'''
		for user in User.objects.all():
			user.set_password('password')
			user.save()
		self.client.login(username='davidkrisch', password='password')
		self.simple_bill = {'name': 'Grocery Shopping', 'amount': '64.57',
				'date': '2010-07-20', 'is_paid': False}
		self.recurring_bill = {'name': 'Gym Membership', 'amount': '39.90',
				'date': '2010-07-20', 'is_paid': False, 'does_repeat': 'true', 
				'repeat_every': 1, 'has_end': 'until', 'end_date': '2011-10-15'}


	def test_create_bill_get(self):
		"""Test that GET returns a form with the proper template context"""
		response = self.client.get('/create/')
		self.assertTemplateUsed(response, 'bills_form.html')
		self.assertTrue(response.context[0].has_key('bill_form'))
		self.assertTrue(response.context[0].has_key('recurrence_form'))

	def test_create_simple_bill(self):
		"""Test that create bill adds a single new bill"""
		response = self.client.post('/create/', self.simple_bill, follow=True)
		self.assertRedirects(response, '/list/')
		bills = Bill.objects.all()
		self.assertEqual(1, len(bills))
		bill = bills[0]
		self.assertEqual(self.simple_bill['name'], bill.name) 
		self.assertEqual(get_date(self.simple_bill['date']), bill.date) 
		self.assertEqual(Decimal(self.simple_bill['amount']), bill.amount) 
		self.assertEqual(self.simple_bill['is_paid'], bill.is_paid) 

	def test_create_recurring_bill_monthly(self):
		"""Test that creating a recurring bill adds a single new bill - monthly"""
		self.recurring_bill['repeats'] = 'monthly'
		self.recurring_bill['repeat_by'] = 'day_of_month'
		response = self.client.post('/create/', self.recurring_bill, follow=True) 
		bills = Bill.objects.all()
		self.assertEqual(1, len(bills))
		bill = bills[0]
		self.assertEqual(self.recurring_bill['name'], bill.name) 
		self.assertEqual(get_date(self.recurring_bill['date']), bill.date) 
		self.assertEqual(Decimal(self.recurring_bill['amount']), bill.amount) 
		self.assertEqual(self.recurring_bill['is_paid'], bill.is_paid) 
		recurrences = Recurrence.objects.all()
		self.assertEqual(1, len(recurrences))
		as_list = recurrences[0].as_list()
		self.assertEqual(1, len(as_list))
		date = as_list[0]
		self.assertEqual(datetime(2010, 11, 1), date)

	def test_create_recurring_bill_monthly_by_day_of_week(self):
		"""Test that creating a recurring bill adds a single new bill - monthly - by day of week
				An example is monthly on the third Tuesday of the month	
		"""
		self.recurring_bill['repeats'] = 'monthly'
		self.recurring_bill['repeat_by'] = 'day_of_week'
		response = self.client.post('/create/', self.recurring_bill, follow=True) 
		bills = Bill.objects.all()
		self.assertEqual(1, len(bills))
		bill = bills[0]
		self.assertEqual(self.recurring_bill['name'], bill.name) 
		self.assertEqual(get_date(self.recurring_bill['date']), bill.date) 
		self.assertEqual(Decimal(self.recurring_bill['amount']), bill.amount) 
		self.assertEqual(self.recurring_bill['is_paid'], bill.is_paid) 
		recurrences = Recurrence.objects.all()
		self.assertEqual(1, len(recurrences))
		startdate = datetime(2010, 8, 1)
		enddate = datetime(2010, 10, 30)
		as_list = recurrences[0].as_list(start_date=startdate, end_date=enddate)
		self.assertEqual(3, len(as_list))
		self.assertEqual(datetime(2010, 8, 17), as_list[0])
		self.assertEqual(datetime(2010, 9, 21), as_list[1])
		self.assertEqual(datetime(2010, 10, 19), as_list[2])

	def test_create_recurring_bill_weekly(self):
		"""Test that creating a recurring bill adds a single new bill - weekly"""
		self.recurring_bill['repeats'] = 'weekly',
		# Create a bill that occurs weekly on Tuesday
		self.recurring_bill['repeat_on'] = ['TU']
		response = self.client.post('/create/', self.recurring_bill, follow=True) 
		bills = Bill.objects.all()
		self.assertEqual(1, len(bills))
		bill = bills[0]
		self.assertEqual(self.recurring_bill['name'], bill.name) 
		self.assertEqual(get_date(self.recurring_bill['date']), bill.date) 
		self.assertEqual(Decimal(self.recurring_bill['amount']), bill.amount) 
		self.assertEqual(self.recurring_bill['is_paid'], bill.is_paid) 
		recurrences = Recurrence.objects.all()
		self.assertEqual(1, len(recurrences))
		# Make sure it occurs 2 times between 10/30/2010 and 11/14/2010
		startdate = datetime(2010, 10, 30)
		enddate = datetime(2010, 11, 14)
		as_list = recurrences[0].as_list(start_date=startdate, end_date=enddate)
		self.assertEqual(2, len(as_list))
		self.assertEqual(datetime(2010, 11, 2), as_list[0])
		self.assertEqual(datetime(2010, 11, 9), as_list[1])

	def test_create_recurring_bill_weekly_twice_a_week(self):
		"""Test that creating a recurring bill adds a single new bill - weekly"""
		self.recurring_bill['repeats'] = 'weekly',
		# Create a bill that occurs weekly on Tuesday, Thursday
		self.recurring_bill['repeat_on'] = ['TU', 'TH']
		response = self.client.post('/create/', self.recurring_bill, follow=True) 
		bills = Bill.objects.all()
		self.assertEqual(1, len(bills))
		bill = bills[0]
		self.assertEqual(self.recurring_bill['name'], bill.name) 
		self.assertEqual(get_date(self.recurring_bill['date']), bill.date) 
		self.assertEqual(Decimal(self.recurring_bill['amount']), bill.amount) 
		self.assertEqual(self.recurring_bill['is_paid'], bill.is_paid) 
		recurrences = Recurrence.objects.all()
		self.assertEqual(1, len(recurrences))
		# Make sure it occurs 4 times between 10/30/2010 and 11/15/2010
		startdate = datetime(2010, 10, 30)
		enddate = datetime(2010, 11, 15)
		as_list = recurrences[0].as_list(start_date=startdate, end_date=enddate)
		self.assertEqual(4, len(as_list))
		self.assertEqual(datetime(2010, 11, 2), as_list[0])
		self.assertEqual(datetime(2010, 11, 4), as_list[1])
		self.assertEqual(datetime(2010, 11, 9), as_list[2])
		self.assertEqual(datetime(2010, 11, 11), as_list[3])
