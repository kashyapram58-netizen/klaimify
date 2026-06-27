import frappe

def execute(filters=None):
    columns = [
        {"fieldname": "member", "fieldtype": "Link", "label": "Member", "options": "Library Member", "width": 150},
        {"fieldname": "total_outstanding", "fieldtype": "Currency", "label": "Total Outstanding", "width": 150},
        {"fieldname": "pending_fines", "fieldtype": "Int", "label": "Pending Fines", "width": 120}
    ]

    # Aggregating fines by member
    data = frappe.db.sql("""
        SELECT 
            member, 
            SUM(amount) as total_outstanding, 
            COUNT(name) as pending_fines 
        FROM `tabLibrary Fine` 
        WHERE status = 'Unpaid' 
        GROUP BY member
    """, as_dict=True)

    return columns, data