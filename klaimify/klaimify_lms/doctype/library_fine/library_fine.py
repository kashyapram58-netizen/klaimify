# Copyright (c) 2026, Ram and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LibraryFine(Document):
	# Add this logic to your library_fine.py
	def validate(self):
		# 1. Handle Waiver
		if self.is_waived:
			self.amount = 0
			self.status = "Waived"
			return # Stop here if waived

		# 2. Handle Payment logic
		if self.paid_amount >= self.amount:
			self.status = "Paid"
		else:
			self.status = "Unpaid"
		
