from django.contrib import admin
from models import Bill, Recurrence

class RecurrenceInlineAdmin(admin.StackedInline):
	model = Recurrence

class BillAdmin(admin.ModelAdmin):
	inlines = [RecurrenceInlineAdmin,]

admin.site.register(Bill, BillAdmin)
