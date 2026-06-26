import frappe
from frappe.utils import today, date_diff

def generate_overdue_fines():
    # Find all transactions that are 'Issued', past the due_date, and not yet returned
    overdue_transactions = frappe.get_all(
        "Library Transaction",
        filters={
            "status": "Issued",
            "due_date": ["<", today()]
        }
    )
    
    for tx in overdue_transactions:
        # Check if fine already exists to avoid duplicates
        existing_fine = frappe.db.exists("Library Fine", {"transaction": tx.name})
        
        if not existing_fine:
            # Create a new Fine record
            fine = frappe.get_doc({
                "doctype": "Library Fine",
                "member": frappe.db.get_value("Library Transaction", tx.name, "member"),
                "transaction": tx.name,
                "amount": 50, # Example: 50 units per day or fixed
                "status": "Unpaid"
            })
            fine.insert()
            frappe.db.commit()