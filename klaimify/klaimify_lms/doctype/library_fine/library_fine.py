# Copyright (c) 2026, Ram and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LibraryFine(Document):
    def validate(self):
        # 1. Handle Waiver
        if self.is_waived:
            self.amount = 0
            self.status = "Waived"
            return 

        # 2. Handle Status based on payment
        if self.paid_amount >= self.amount:
            self.status = "Paid"
        elif self.paid_amount > 0:
            self.status = "Partially Paid"    
        else:
            self.status = "Unpaid"

    def on_submit(self):
        # Post "Fine Raised" entry only once when submitted
        self.create_journal_entry("Fine Raised", self.amount, is_payment=False)
    def on_update(self):
        # Only post payment if status is Paid and no payment entry exists
       if self.paid_amount > 0 and self.docstatus == 1:
            remark = f"Payment of {self.paid_amount} for Fine: {self.name}"
            # Check if this fine already has a payment journal entry to prevent duplicates
            if not frappe.db.exists("Journal Entry", {"remark": remark}):
               self.create_journal_entry(f"Payment Received", self.paid_amount, is_payment=True)

    def create_journal_entry(self, title, amount, is_payment):
        income_account = "Fine - KD"
        cash_account = "Cash - KD" # Use a cash/bank account here
        receivable_account = "Library Accounts Receivable - KD"
        if is_payment:
            entries = [
                {"account": cash_account, "debit_in_account_currency": amount, "credit_in_account_currency": 0},
                {"account": receivable_account, "debit_in_account_currency": 0, "credit_in_account_currency": amount}
			]
        else:
            entries = [
                {"account": receivable_account, "debit_in_account_currency": amount, "credit_in_account_currency": 0}, # Temp placeholder
                {"account": income_account, "debit_in_account_currency": 0, "credit_in_account_currency": amount}
			]
        # Create Journal Entry
        je = frappe.get_doc({
            "doctype": "Journal Entry",
            "voucher_type": "Journal Entry",
            "posting_date": frappe.utils.today(),
            "remark": f"{title} for Fine: {self.name}", # Crucial for finding the entry later
            "accounts": entries
            
        })
        je.flags.ignore_permissions = True
        je.insert()
        je.submit()