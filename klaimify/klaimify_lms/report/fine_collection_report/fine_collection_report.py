import frappe

def execute(filters=None):
    columns = [
        {"fieldname": "member", "fieldtype": "Link", "label": "Member", "options": "Library Member", "width": 150},
        {"fieldname": "total_raised", "fieldtype": "Currency", "label": "Total Raised", "width": 150},
        {"fieldname": "total_collected", "fieldtype": "Currency", "label": "Total Collected", "width": 150},
        {"fieldname": "outstanding", "fieldtype": "Currency", "label": "Balance", "width": 150}
    ]

    # Query to sum fines raised vs fines collected
    data = frappe.db.sql("""
        SELECT 
            member, 
            SUM(amount) as total_raised, 
            SUM(paid_amount) as total_collected,
            (SUM(amount) - SUM(paid_amount)) as outstanding
        FROM `tabLibrary Fine` 
        GROUP BY member
    """, as_dict=True)

    return columns, data