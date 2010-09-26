from django.test import TestCase
from django.test.client import Client
from django.forms.models import model_to_dict
from billtally.site.models import Bill
import json

class BillAPITest(TestCase):
	fixtures = ['bills.json']

	def test_simple_create(self):
		test_bill = {'name': 'Grocery Shopping', 
								 'amount': '65.35',
								 'date': '2010-10-14', 
								 'is_paid': False}

		num_bills_before = Bill.objects.count()
		response = self.client.post('/api/bills', test_bill, follow=True)
		self.assertEqual(response.status_code, 200)
		num_bills_after = Bill.objects.count()
		self.assertEqual(num_bills_before + 1, num_bills_after)
		json_response = json.loads(response.content)
		self.assertEqual(test_bill.get('name'), json_response.get('name'))

	def test_simple_read(self):
		response = self.client.get('/api/bills?format=json')
		self.assertEqual(response.status_code, 200)
		json_response = json.loads(response.content)
		self.assertEquals(len(json_response), 4)

	def test_simple_update(self):
		new_name = 'New Bill Name'
		test_bill = Bill.objects.all()[0]
		test_bill.name = new_name
		response = self.client.put('/api/bills/%i/' % test_bill.id, model_to_dict(test_bill))
		self.assertEqual(response.status_code, 200)

		# Verify the returned bill has the correct new name
		json_response = json.loads(response.content)
		self.assertEqual(json_response.get('name'), new_name)

		# Verify the bill was updated in the database
		bill = Bill.objects.get(name=new_name)
		self.assertEqual(bill.name, new_name)
		self.assertEqual(bill.date, test_bill.date) 

	def test_simple_delete(self):
		bills = Bill.objects.all()
		num_bills_before = len(bills)
		response = self.client.delete('/api/bills/%i/' % bills[0].id, follow=True)
		self.assertEqual(response.status_code, 204)
		self.assertEqual(num_bills_before - 1, Bill.objects.count())
