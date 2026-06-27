import frappe
from frappe.utils import today, date_diff

def generate_overdue_fines():
    # 1. Fetch only what we need in one query
    overdue_transactions = frappe.get_all(
        "Library Transaction",
        filters={
            "status": "Issued",
            "due_date": ["<", today()]
        },
        fields=["name", "member", "due_date"]
    )
    
    daily_rate = 10  # Define your fine per day
    
    for tx in overdue_transactions:
        # Check if fine already exists
        if not frappe.db.exists("Library Fine", {"transaction": tx.name}):
            # 2. Calculate dynamic fine
            days_overdue = date_diff(today(), tx.due_date)
            total_fine = days_overdue * daily_rate
            
            # 3. Create Fine record
            fine = frappe.get_doc({
                "doctype": "Library Fine",
                "member": tx.member,
                "transaction": tx.name,
                "amount": total_fine,
                "status": "Unpaid"
            })
            # Use ignore_permissions=True to ensure system can create it
            fine.insert(ignore_permissions=True)
            
    # Commit once at the end
    frappe.db.commit()