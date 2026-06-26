# Copyright (c) 2026, Ram and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_days, today

class LibraryTransaction(Document):
    def before_save(self):
        # 1. Automate Due Date (14 days)
        if self.issue_date and not self.due_date:
            self.due_date = add_days(self.issue_date, 14)
            
        # 2. Default Status
        if not self.status:
            self.status = 'Issued'

    def after_save(self):
        # 3. Handle Inventory Updates
        if self.status == 'Issued':
            self.update_book_copy_status(self.book, self.copy_id, 'Issued')
        elif self.status == 'Returned':
            self.update_book_copy_status(self.book, self.copy_id, 'Available')

    def update_book_copy_status(self, book_name, copy_id, new_status):
        book = frappe.get_doc("Library Book", book_name)
        for copy in book.copies:
            if copy.copy_id == copy_id:
                copy.status = new_status
        book.save()
