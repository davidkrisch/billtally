from django.test import TestCase, Client
from billtally.site.models import Bill, Recurrence
from django.contrib.auth.models import User

class BillTest(TestCase):
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
		self.assertTrue('list.html' in [template.name for template in response.template])
		self.assertTrue(len(response.context['unpaid']) == 1)
		self.assertTrue(len(response.context['paid']) == 2)
		self.assertTrue(len(response.context['overdue']) == 1)

	def test_create_bill(self):
		"""Test that create bill adds a single new bill"""
		num_bills_before = Bill.objects.count()
		response = self.client.post('/create/', 
				{'name': 'Grocery Shopping', 'amount': '64.57', 'date': '07/10/2010',
					'is_paid': False, 'is_recurring': False}, follow=True)
		self.failUnlessEqual(response.status_code, 200)
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
