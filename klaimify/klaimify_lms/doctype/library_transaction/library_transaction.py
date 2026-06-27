import frappe
from frappe.model.document import Document
from frappe.utils import add_days, today

class LibraryTransaction(Document):
    def validate(self):
        # Always call validation first to prevent invalid transactions
        self.validate_membership()

    def before_save(self):
        # 1. Automate Due Date (14 days)
        if self.issue_date and not self.due_date:
            self.due_date = add_days(self.issue_date, 14)
            
        # 2. Default Status
        if not self.status:
            self.status = 'Issued'

    def on_submit(self):
        # 3. Handle Inventory Updates via Standalone DocType
        if self.status == 'Issued':
            self.update_book_copy_status(self.book_copy, 'Issued')
            
    def on_cancel(self):
        # 4. Revert inventory status if transaction is cancelled
        self.update_book_copy_status(self.book_copy, 'Available')

    def update_book_copy_status(self, copy_id, new_status):
        # Direct database update. No need to loop through the parent book!
        frappe.db.set_value("Library Book Copy", copy_id, "status", new_status)

    def validate_membership(self):
        # Check membership status
        member = frappe.get_doc("Library Member", self.member)
        if member.membership_end_date < today():
            frappe.throw("Membership has expired. Please renew to issue books.")