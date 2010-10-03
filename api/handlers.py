from piston.handler import BaseHandler
from piston.utils import rc
from billtally.site.models import Bill

class BillHandler(BaseHandler):
	allowed_methods = ('GET', 'PUT', 'POST', 'DELETE')
	model = Bill
	exclude = ()

#	def update(self, request, bill_id):
#		import pdb; pdb.set_trace()
#
#		bill = BillForm(request.POST)
#		bill.save()
#		return bill.instance

	def delete(self, request, bill_id):
		bill = Bill.objects.get(id=bill_id)
		bill.delete()
		return rc.DELETED
        
