# Copyright (c) 2026, Ram and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryMember(Document):
	def get_outstanding_fines(self):
			# Calculate sum of unpaid fines for this member
			total_unpaid = frappe.db.sql("""
				SELECT SUM(amount - paid_amount) 
				FROM `tabLibrary Fine` 
				WHERE member = %s AND status != 'Paid'
			""", self.name)[0][0]
			
			return total_unpaid or 0
	
