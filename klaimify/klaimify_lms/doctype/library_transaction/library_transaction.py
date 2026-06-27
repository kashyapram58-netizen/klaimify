import frappe
from frappe.model.document import Document
from frappe.utils import add_days, today, getdate

class LibraryTransaction(Document):
    def validate(self):
        if self.status == "Issued":
            copy_status = frappe.db.get_value("Library Book Copy", self.book_copy, "status")
            if copy_status != "Available":
                frappe.throw(f"This copy ({self.book_copy}) is currently {copy_status} and cannot be issued.")
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
        if member.validity_date < getdate(today()):
            frappe.throw("Membership has expired. Please renew to issue books.")

    def after_save(self):
        # 3. Handle Inventory Updates (Simplified for Standalone DocType)
        # We no longer need to loop through the parent book!
        if self.status == 'Issued':
            frappe.db.set_value("Library Book Copy", self.book_copy, "status", "Issued")
        elif self.status == 'Returned':
            frappe.db.set_value("Library Book Copy", self.book_copy, "status", "Available")


    def mark_overdue_transactions():
        # 1. Find all issued books where due_date is in the past
        overdue_transactions = frappe.get_all("Library Transaction", filters={
            "status": "Issued",
            "due_date": ["<", today()]
        }, fields=["name"])

        # 2. Update their status to 'Overdue'
        for transaction in overdue_transactions:
            frappe.db.set_value("Library Transaction", transaction.name, "status", "Overdue")
        
        # 3. Commit changes to the database
        frappe.db.commit()                