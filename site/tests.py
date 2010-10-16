from django.test import TestCase, Client
from billtally.site.models import Bill, Recurrence
from django.contrib.auth.models import User
from datetime import datetime
from dateutil.relativedelta import relativedelta

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
		self.assertTrue(Bill.objects.count(), 1)
		self.assertTrue(bill.recurrence_set.count(), 1)

	def test_as_list(self):
		'''Test the Bill Model's as_rrule method'''
		bill = Bill(**self.bill_data)
		bill.save()
		recurrence = Recurrence(**self.recurrence_data)
		recurrence.bill = bill
		recurrence.save()
		r_list = recurrence.as_list()
		self.assertEquals(len(r_list), 1)  

		# The next due date should be the first day of next month
		expected = datetime.today() + relativedelta(day=1, months=+1)
		self.assertEquals(r_list[0].date(), expected.date())

	def test_as_list_with_startdate(self):
		'''Test as_list with a start date'''
		bill = Bill(**self.bill_data)
		bill.save()
		recurrence = Recurrence(**self.recurrence_data)
		recurrence.bill = bill
		recurrence.save()
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
		start = datetime(2010, 11, 15)
		end = datetime(2010, 12, 15)
		r_list = recurrence.as_list(start_date=start, end_date=end)
		self.assertEquals(len(r_list), 1)
		self.assertEquals(r_list[0].date(), datetime(2010, 12, 1).date())

class BillViewTest(TestCase):
	fixtures = ['bills.json']

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

	def test_create_bill_get(self):
		"""Test that GET returns a form with the proper template context"""
		response = self.client.get('/create/')
		self.assertTemplateUsed(response, 'bills_form.html')
		self.assertTrue(response.context[0].has_key('bill_form'))
		self.assertTrue(response.context[0].has_key('recurrence_form'))

	def test_create_simple_bill(self):
		"""Test that create bill adds a single new bill"""
		num_bills_before = Bill.objects.count()
		response = self.client.post('/create/', 
				{'name': 'Grocery Shopping', 'amount': '64.57', 'date': '07/10/2010',
					'is_paid': False, 'is_recurring': False}, follow=True)
		self.assertRedirects(response, '/list/')
		num_bills_after = Bill.objects.count()
		self.assertEqual(num_bills_before + 1, num_bills_after)

#class RecurringBillTest(TestCase):
#	fixtures = ['bills.json']
#
#	def test_create_recurring_bill(self):
#		"""Test that creating a recurring bill adds a single new bill"""
#		num_bills_before = RecurringBill.objects.count()
#		response = self.client.post('/create/',
#				{'name': 'Gym Membership', 'amount': '39.90', 'date': '07/20/2010',
#					'is_paid': False, 'is_recurring': True, }, follow=True) 
