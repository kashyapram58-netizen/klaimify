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
        else:
            self.status = "Unpaid"

    def on_submit(self):
        # Post "Fine Raised" entry only once when submitted
        self.create_journal_entry("Fine Raised", self.amount)

    def on_update(self):
        # Only post payment if status is Paid and no payment entry exists
        if self.status == "Paid" and self.paid_amount > 0:
            # Check if this fine already has a payment journal entry to prevent duplicates
            if not frappe.db.exists("Journal Entry", {"remark": f"Payment for Fine: {self.name}"}):
                self.create_journal_entry("Payment Received", self.paid_amount)

    def create_journal_entry(self, title, amount):
        income_account = "Fine - KD"
        cash_account = "Cash - KD" # Use a cash/bank account here
        # Create Journal Entry
        je = frappe.get_doc({
            "doctype": "Journal Entry",
            "voucher_type": "Journal Entry",
            "posting_date": frappe.utils.today(),
            "remark": f"{title} for Fine: {self.name}", # Crucial for finding the entry later
            "accounts": [
                {
                    "account": income_account,
                    "credit_in_account_currency": amount if title == "Fine Raised" else 0,
                    "debit_in_account_currency": 0 if title == "Fine Raised" else amount,
                    # "party_type": "Customer",
                    # "party": self.member, 
                },
                {
                    "account": cash_account, 
                    "debit_in_account_currency": amount if title == "Fine Raised" else 0,
                    "credit_in_account_currency": 0 if title == "Fine Raised" else amount,
                }
            ]
        })
        je.flags.ignore_permissions = True
        je.insert()
        je.submit()