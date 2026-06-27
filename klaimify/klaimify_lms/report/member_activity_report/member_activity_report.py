import frappe

def execute(filters=None):
    columns = [
        {"fieldname": "member", "label": "Member", "fieldtype": "Link", "options": "Library Member", "width": 150},
        {"fieldname": "book", "label": "Book", "fieldtype": "Data", "width": 200},
        {"fieldname": "issue_date", "label": "Issue Date", "fieldtype": "Date", "width": 100},
        {"fieldname": "due_date", "label": "Due Date", "fieldtype": "Date", "width": 100},
        {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 100}
    ]

    # Build the base query
    conditions = ""
    if filters and filters.get("member"):
        conditions = "AND member = %(member)s"

    data = frappe.db.sql(f"""
        SELECT 
            member, book, issue_date, due_date, status
        FROM 
            `tabLibrary Transaction`
        WHERE 
            1=1 {conditions}
        ORDER BY 
            issue_date DESC
    """, filters, as_dict=True)

    return columns, data